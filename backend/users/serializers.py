from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, RoleOfUser, DeliveryAddress

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def create(self, validated_data):
    # Автоматически назначаем роль "Пользователь" при регистрации
        customer_role = RoleOfUser.objects.get(role_name='Пользователь')
        
        # Создаём пользователя без поля username
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=customer_role
        )
        # Хешируем пароль
        user.set_password(validated_data['password'])
        user.save()
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """Для просмотра и редактирования профиля"""
    role_name = serializers.CharField(source='role.role_name', read_only=True)
    
    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email', 'phone', 'role_name')
        read_only_fields = ('user_id', 'email', 'role_name')


class LoginSerializer(TokenObtainPairSerializer):
    """
    Кастомный сериализатор для получения JWT токенов.
    Автоматически использует email как USERNAME_FIELD.
    """
    
    def validate(self, attrs):
        # Simple JWT автоматически использует USERNAME_FIELD = 'email'
        # Ничего дополнительно делать не нужно!
        data = super().validate(attrs)
        
        # Добавляем дополнительную информацию о пользователе в ответ
        data['user'] = {
            'user_id': self.user.user_id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'role': self.user.role.role_name if self.user.role else None,
        }
        
        return data


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = ('address_id', 'city', 'street', 'house', 'apartment')
        read_only_fields = ('address_id',)
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)