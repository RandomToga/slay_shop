from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Order, OrderStatus
from .serializers import OrderSerializer, OrderStatusUpdateSerializer
from slay_api.permissions import IsManager

class OrderCreateView(generics.CreateAPIView):
    """
    POST /api/orders/ — оформить заказ.
    Принимает address_id и payment_method_id.
    """
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        # После создания сериализуем готовый заказ для ответа
        response_serializer = OrderSerializer(order, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class UserOrderListView(generics.ListAPIView):
    """
    GET /api/orders/ — история заказов текущего пользователя.
    """
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'items__product', 'order_status', 'payment_method', 'delivery_address'
        ).order_by('-order_date')


class UserOrderDetailView(generics.RetrieveAPIView):
    """
    GET /api/orders/{id}/ — детали конкретного заказа пользователя.
    """
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'order_id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'items__product', 'order_status', 'payment_method', 'delivery_address'
        )


# --- Административные представления ---

class AdminOrderListView(generics.ListAPIView):
    """
    GET /api/admin/orders/ — список всех заказов с фильтром по статусу.
    """
    serializer_class = OrderSerializer
    permission_classes = (IsManager,)

    def get_queryset(self):
        queryset = Order.objects.all().prefetch_related(
            'items__product', 'order_status', 'payment_method', 'delivery_address', 'user'
        ).order_by('-order_date')

        status_filter = self.request.query_params.get('status')
        if status_filter:
            # Фильтруем по status_id или status_name – удобнее по id
            try:
                status_id = int(status_filter)
                queryset = queryset.filter(order_status__status_id=status_id)
            except ValueError:
                queryset = queryset.filter(order_status__status_name__iexact=status_filter)

        return queryset


class AdminOrderDetailView(generics.RetrieveAPIView):
    """
    GET /api/admin/orders/{id}/ — детали любого заказа.
    """
    serializer_class = OrderSerializer
    permission_classes = (IsManager,)
    lookup_field = 'order_id'
    lookup_url_kwarg = 'id'
    queryset = Order.objects.all().prefetch_related(
        'items__product', 'order_status', 'payment_method', 'delivery_address', 'user'
    )


class AdminOrderStatusUpdateView(generics.UpdateAPIView):
    """
    PATCH /api/admin/orders/{id}/status/ — изменить статус заказа.
    """
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = (IsManager,)
    lookup_field = 'order_id'
    lookup_url_kwarg = 'id'
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # PATCH всегда частичный
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # Возвращаем полный заказ после обновления статуса
        full_serializer = OrderSerializer(instance, context={'request': request})
        return Response(full_serializer.data)