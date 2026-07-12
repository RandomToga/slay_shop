from rest_framework import serializers

from catalog.models import Product
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
    )
    product_name = serializers.CharField(source='product.product_name', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(source='subtotal', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ('cart_item_id', 'product_id', 'product_name', 'product_quantity', 'price', 'total_price')
        read_only_fields = ('cart_item_id',)

    def validate(self, attrs):
        product = attrs.get('product') or getattr(self.instance, 'product', None)
        product_quantity = attrs.get('product_quantity', getattr(self.instance, 'product_quantity', 1))

        if product_quantity < 1:
            raise serializers.ValidationError('Количество товара должно быть больше 0.')
        if product and product_quantity > product.stock_quantity:
            raise serializers.ValidationError('Количество товара превышает остаток на складе.')

        return attrs

    def create(self, validated_data):
        cart, _ = Cart.objects.get_or_create(user=self.context['request'].user)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=validated_data['product'],
            defaults={'product_quantity': validated_data.get('product_quantity', 1)},
        )

        if not created:
            item.product_quantity += validated_data.get('product_quantity', 1)
            if item.product_quantity > item.product.stock_quantity:
                raise serializers.ValidationError('Количество товара превышает остаток на складе.')
            item.save(update_fields=('product_quantity',))

        return item


class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.user_id', read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(source='total_price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ('cart_id', 'user_id', 'items', 'total_amount', 'creation_date', 'update_date')
