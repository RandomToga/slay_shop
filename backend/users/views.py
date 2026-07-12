from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, DeliveryAddressSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, DeliveryAddress
from cart.views import merge_session_cart_to_user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'Регистрация успешна',
            'user': {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        }, status=status.HTTP_201_CREATED)
    


class LoginView(TokenObtainPairView):
    """
    Универсальный вход для ВСЕХ пользователей.
    Просто принимает email и пароль, возвращает токены.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as exc:
            raise InvalidToken(exc.args[0])

        merge_session_cart_to_user(request, serializer.user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



class UserDetailView(generics.RetrieveUpdateAPIView):
    """Просмотр и редактирование своего профиля"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Пользователь видит только свои адреса
        return DeliveryAddress.objects.filter(user=self.request.user, is_deleted=False)
    
    def perform_destroy(self, instance):
        # Мягкое удаление
        instance.is_deleted = True
        instance.save()