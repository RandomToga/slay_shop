from django.db import transaction
from rest_framework import serializers

from cart.models import Cart
from .models import Order, OrderItem, OrderStatus, PaymentMethod
from users.models import DeliveryAddress
from users.serializers import DeliveryAddressSerializer


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ('payment_method_id', 'payment_method_name')


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ('status_id', 'status_name', 'status_description')


class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.product_id', read_only=True)
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    price_at_order = serializers.DecimalField(
        source='product_price_at_order', max_digits=10, decimal_places=2, read_only=True
    )
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = (
            'order_item_id', 'product_id', 'product_name',
            'product_quantity', 'price_at_order', 'subtotal',
        )

    def get_subtotal(self, obj):
        return obj.product_price_at_order * obj.product_quantity


class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.user_id', read_only=True)
    status = OrderStatusSerializer(source='order_status', read_only=True)
    payment_method = PaymentMethodSerializer(read_only=True)
    payment_method_id = serializers.PrimaryKeyRelatedField(
        queryset=PaymentMethod.objects.all(),
        source='payment_method',
        write_only=True,
    )
    address_id = serializers.PrimaryKeyRelatedField(
        queryset=DeliveryAddress.objects.all(),
        source='delivery_address',
        write_only=True,
    )
    delivery_address = DeliveryAddressSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = (
            'order_id', 'user_id', 'status', 'payment_method',
            'payment_method_id', 'address_id', 'delivery_address',
            'total_amount', 'items', 'order_date',
        )
        read_only_fields = ('order_id', 'user_id', 'total_amount', 'order_date')

    def validate_address_id(self, value):
        user = self.context['request'].user
        if value.user != user:
            raise serializers.ValidationError('Вы можете использовать только свои адреса доставки.')
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        cart = Cart.objects.filter(user=user).prefetch_related('items__product').first()

        if not cart or not cart.items.exists():
            raise serializers.ValidationError({'cart': 'Корзина пуста, заказ оформить невозможно.'})

        for item in cart.items.select_related('product'):
            product = item.product
            if item.product_quantity > product.stock_quantity:
                raise serializers.ValidationError({
                    'cart': f'Недостаточно товара "{product.product_name}" на складе. '
                            f'Доступно: {product.stock_quantity}, запрошено: {item.product_quantity}'
                })

        self._cart = cart
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        cart = self._cart

        initial_status = OrderStatus.objects.filter(status_name='Новый').first()
        if not initial_status:
            # fallback: берём первый попавшийся или создаём
            initial_status = OrderStatus.objects.first()
            if not initial_status:
                initial_status = OrderStatus.objects.create(status_name='Новый')

        with transaction.atomic():
            # Создаём заказ
            order = Order.objects.create(
                user=user,
                order_status=initial_status,
                payment_method=validated_data['payment_method'],
                delivery_address=validated_data['delivery_address'],
                total_amount=cart.total_price,
            )

            # Переносим позиции корзины в заказ и обновляем остатки
            for cart_item in cart.items.select_related('product'):
                product = cart_item.product
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_quantity=cart_item.product_quantity,
                    product_price_at_order=product.price,
                )
                # Уменьшаем остаток на складе
                product.stock_quantity -= cart_item.product_quantity
                product.save(update_fields=('stock_quantity',))

            # Очищаем корзину
            cart.items.all().delete()

        return order


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Только для обновления статуса заказа менеджером."""
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=OrderStatus.objects.all(),
        source='order_status',
    )

    class Meta:
        model = Order
        fields = ('status_id',)

    def update(self, instance, validated_data):
        instance.order_status = validated_data['order_status']
        instance.save(update_fields=('order_status',))
        return instance