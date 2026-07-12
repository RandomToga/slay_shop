from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Product
from .models import Cart, CartItem
from .serializers import CartItemSerializer, CartSerializer


CART_SESSION_KEY = 'cart'


def _get_session_cart(request):
    return request.session.get(CART_SESSION_KEY, {})


def _save_session_cart(request, cart_data):
    request.session[CART_SESSION_KEY] = {
        str(product_id): int(quantity)
        for product_id, quantity in cart_data.items()
        if int(quantity) > 0
    }
    request.session.modified = True


def _empty_cart_data(user=None):
    return {
        'cart_id': None,
        'user_id': getattr(user, 'user_id', None),
        'items': [],
        'total_amount': 0,
        'creation_date': None,
        'update_date': None,
    }


def _serialize_guest_cart(request):
    cart_data = _get_session_cart(request)
    products = Product.objects.filter(product_id__in=cart_data.keys())
    products_by_id = {str(product.product_id): product for product in products}

    items = []
    total_amount = 0
    valid_cart_data = {}

    for product_id, quantity in cart_data.items():
        product = products_by_id.get(str(product_id))
        if product is None:
            continue

        quantity = int(quantity)
        item = CartItem(product=product, product_quantity=quantity)
        item_data = CartItemSerializer(item).data
        item_data['cart_item_id'] = product.product_id
        items.append(item_data)
        total_amount += item.subtotal
        valid_cart_data[product_id] = quantity

    if valid_cart_data != cart_data:
        _save_session_cart(request, valid_cart_data)

    return {
        'cart_id': None,
        'user_id': None,
        'items': items,
        'total_amount': f'{total_amount:.2f}',
        'creation_date': None,
        'update_date': None,
    }


def _serialize_user_cart(user):
    cart = Cart.objects.filter(user=user).prefetch_related('items__product').first()
    if cart is None:
        return _empty_cart_data(user)
    return CartSerializer(cart).data


def merge_session_cart_to_user(request, user):
    cart_data = _get_session_cart(request)
    if not cart_data:
        return

    with transaction.atomic():
        cart, _ = Cart.objects.get_or_create(user=user)
        products = Product.objects.filter(product_id__in=cart_data.keys())
        products_by_id = {str(product.product_id): product for product in products}

        for product_id, quantity in cart_data.items():
            product = products_by_id.get(str(product_id))
            if product is None:
                continue

            quantity = int(quantity)
            item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'product_quantity': min(quantity, product.stock_quantity)},
            )
            if not created:
                item.product_quantity = min(item.product_quantity + quantity, product.stock_quantity)
                item.save(update_fields=('product_quantity',))

    _save_session_cart(request, {})


class CartView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            return Response(_serialize_user_cart(request.user))
        return Response(_serialize_guest_cart(request))


class CartClearView(APIView):
    permission_classes = (permissions.AllowAny,)

    def delete(self, request):
        if request.user.is_authenticated:
            Cart.objects.filter(user=request.user).delete()
        else:
            _save_session_cart(request, {})

        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            merge_session_cart_to_user(request, request.user)
            return super().create(request, *args, **kwargs)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('product_quantity', 1)

        cart_data = _get_session_cart(request)
        new_quantity = int(cart_data.get(str(product.product_id), 0)) + quantity
        if new_quantity > product.stock_quantity:
            return Response(
                {'detail': 'Количество товара превышает остаток на складе.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_data[str(product.product_id)] = new_quantity
        _save_session_cart(request, cart_data)
        return Response(_serialize_guest_cart(request), status=status.HTTP_201_CREATED)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = (permissions.AllowAny,)
    http_method_names = ('patch', 'delete', 'head', 'options')
    lookup_field = 'cart_item_id'
    lookup_url_kwarg = 'item_id'

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return CartItem.objects.none()

        cart = Cart.objects.filter(user=self.request.user).first()
        if cart is None:
            return CartItem.objects.none()

        return CartItem.objects.filter(cart=cart).select_related('product')

    def patch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().patch(request, *args, **kwargs)

        product_id = str(kwargs['item_id'])
        cart_data = _get_session_cart(request)
        if product_id not in cart_data:
            return Response({'detail': 'Позиция корзины не найдена.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data.get('product_quantity')
        if quantity is None:
            return Response({'detail': 'Передайте product_quantity.'}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.filter(product_id=product_id).first()
        if product is None:
            return Response({'detail': 'Товар не найден.'}, status=status.HTTP_404_NOT_FOUND)
        if quantity > product.stock_quantity:
            return Response(
                {'detail': 'Количество товара превышает остаток на складе.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart_data[product_id] = quantity
        _save_session_cart(request, cart_data)
        return Response(_serialize_guest_cart(request))

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().delete(request, *args, **kwargs)

        cart_data = _get_session_cart(request)
        cart_data.pop(str(kwargs['item_id']), None)
        _save_session_cart(request, cart_data)
        return Response(status=status.HTTP_204_NO_CONTENT)
