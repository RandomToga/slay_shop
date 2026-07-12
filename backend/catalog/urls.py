from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router_public = DefaultRouter()
router_public.register(r'products', views.PublicProductViewSet, basename='public-product')
router_public.register(r'categories', views.PublicCategoryViewSet, basename='public-category')
router_public.register(r'brands', views.PublicBrandViewSet, basename='public-brand')

router_admin = DefaultRouter()
router_admin.register(r'products', views.AdminProductViewSet, basename='admin-product')
router_admin.register(r'categories', views.AdminCategoryViewSet, basename='admin-category')
router_admin.register(r'brands', views.AdminBrandViewSet, basename='admin-brand')

urlpatterns = [
    # Публичные эндпоинты
    path('api/', include(router_public.urls)),
    # Административные эндпоинты
    path('api/admin/', include(router_admin.urls)),
]