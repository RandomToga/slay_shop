from django.urls import path

from .views import CartClearView, CartItemCreateView, CartItemDetailView, CartView


urlpatterns = [
    path('api/cart/', CartView.as_view(), name='cart'),
    path('api/cart/items/', CartItemCreateView.as_view(), name='cart-item-create'),
    path('api/cart/items/<int:item_id>/', CartItemDetailView.as_view(), name='cart-item-detail'),
    path('api/cart/clear/', CartClearView.as_view(), name='cart-clear'),
]
