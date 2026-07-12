from rest_framework import viewsets, mixins
from .models import ProductCategory, Brand, Product
from .serializers import (
    CategorySerializer, BrandSerializer, 
    ProductSerializer
)
from slay_api.permissions import IsManager

# ========== ПУБЛИЧНЫЕ VIEWSETS (только чтение) ==========

class PublicCategoryViewSet(mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    """
    Публичный просмотр категорий
    """
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer


class PublicBrandViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    Публичный просмотр брендов
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class PublicProductViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    """
    Публичный просмотр товаров
    """
    queryset = Product.objects.select_related('brand', 'product_category').all().order_by('product_id')
    serializer_class = ProductSerializer


# ========== АДМИНИСТРАТИВНЫЕ VIEWSETS ==========

class AdminCategoryViewSet(viewsets.ModelViewSet):
    """
    Управление категориями (только для менеджеров)
    """
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsManager]  # Только менеджеры


class AdminBrandViewSet(viewsets.ModelViewSet):
    """
    Управление брендами (только для менеджеров)
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsManager]  # Только менеджеры


class AdminProductViewSet(viewsets.ModelViewSet):
    """
    Управление товарами (только для менеджеров)
    """
    queryset = Product.objects.select_related('brand', 'product_category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsManager]  # Только менеджеры