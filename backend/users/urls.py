from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, UserDetailView, DeliveryAddressViewSet

router = DefaultRouter()
router.register(r'addresses', DeliveryAddressViewSet, basename='address')

urlpatterns = [
    path('api/users/register/', RegisterView.as_view(), name='register'),
    path('api/users/login/', LoginView.as_view(), name='login'),
    path('api/users/me/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/', include(router.urls)),
]