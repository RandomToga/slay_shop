from django.urls import path

from . import views

urlpatterns = [
    # Пользовательские эндпоинты
    path('api/orders/', views.UserOrderListView.as_view(), name='user-order-list'),
    path('api/orders/create/', views.OrderCreateView.as_view(), name='user-order-create'),
    path('api/orders/<int:id>/', views.UserOrderDetailView.as_view(), name='user-order-detail'),

    # Административные эндпоинты
    path('api/admin/orders/', views.AdminOrderListView.as_view(), name='admin-order-list'),
    path('api/admin/orders/<int:id>/', views.AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('api/admin/orders/<int:id>/status/', views.AdminOrderStatusUpdateView.as_view(), name='admin-order-status-update'),
]