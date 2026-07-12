from rest_framework import generics, permissions
from orders.models import PaymentMethod, OrderStatus
from orders.serializers import PaymentMethodSerializer, OrderStatusSerializer


class PaymentMethodListView(generics.ListAPIView):
    """
    GET /api/payment-methods/ — список всех доступных способов оплаты.
    """
    queryset = PaymentMethod.objects.all().order_by('payment_method_id')
    serializer_class = PaymentMethodSerializer
    permission_classes = (permissions.IsAuthenticated,)


class OrderStatusListView(generics.ListAPIView):
    """
    GET /api/order-statuses/ — список всех статусов заказа.
    """
    queryset = OrderStatus.objects.all().order_by('status_id')
    serializer_class = OrderStatusSerializer
    permission_classes = (permissions.IsAuthenticated,)