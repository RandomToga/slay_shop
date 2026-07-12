from django.contrib import admin
from .models import RoleOfUser, User, DeliveryAddress

# Регистрируем модель в админке
admin.site.register(RoleOfUser)
admin.site.register(User)
admin.site.register(DeliveryAddress)
