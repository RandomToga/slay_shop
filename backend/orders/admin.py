from django.contrib import admin

from .models import Order, OrderItem, PaymentMethod, OrderStatus

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PaymentMethod)
admin.site.register(OrderStatus)