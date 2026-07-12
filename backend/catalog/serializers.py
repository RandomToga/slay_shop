from rest_framework import serializers
from .models import ProductCategory, Brand, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('category_id', 'category_name', 'category_description')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('brand_id', 'brand_name', 'brand_country', 'brand_description')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'product_id', 'product_name', 'product_description', 'purpose', 
            'price', 'stock_quantity', 'product_image', 'brand', 'product_category',
        )