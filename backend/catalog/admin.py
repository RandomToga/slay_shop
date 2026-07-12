from django.contrib import admin
from .models import ProductCategory, Brand, Product

admin.site.register(ProductCategory)
admin.site.register(Brand)
admin.site.register(Product)