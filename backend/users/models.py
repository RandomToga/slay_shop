from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

class RoleOfUser(models.Model): 

    role_id = models.AutoField(primary_key=True, db_column='role_id', verbose_name='ID роли')
    # role_id = models.AutoField(...)
    # Создает поле целочисленного типа, которое автоматически увеличивается на 1 при каждой новой записи
    # primary_key=True
    # Указывает, что это поле является первичным ключом (Primary Key) таблицы.
    # По умолчанию Django сам создает поле 'id' как первичный ключ, но здесь мы явно указываем свое поле.
    # db_column='role_id'
    # Задает точное имя колонки (столбца) в самой базе данных. По умолчанию Django назвал бы колонку просто 'id'

    role_name = models.CharField(max_length=100, unique=True, db_column='role_name', verbose_name='Название роли')
    
    class Meta:
        # class Meta
        # Внутренний класс Django, который используется для определения метаданных модели.
        # Метаданные — это настройки, которые влияют на то, как Django взаимодействует с базой данных, 
        # но не на сами поля данных.

        db_table = 'role_of_user'
        # db_table
        # Задает точное имя таблицы, которая будет создана в базе данных для этой модели.
        # По умолчанию Django создал бы таблицу с именем вроде 'users_roleofuser'

        verbose_name = 'Роль пользователя'
        # verbose_name
        # Человекочитаемое имя модели в единственном числе.
        # Это имя будет отображаться в интерфейсе администратора Django (Admin panel) вместо технического 'RoleOfUser'.

        verbose_name_plural = 'Роли пользователей'
        # verbose_name_plural
        # Человекочитаемое имя модели во множественном числе.
        # Django автоматически старается образовать множественное число (добавляя 's'), но может ошибиться

    def __str__(self):
        # def __str__(self)
        # Магический метод Python (dunder method). Определяет, как объект выглядит при преобразовании в строку (str()).
        # Это влияет на то, как объект отображается в админ-панели Django, в выпадающих списках, в консоли отладки и т.д.

        return self.role_name
        # return self.role_name
        # Когда вы попросите Python отобразить объект этой модели (например, объект роли), он вернет значение поля role_name.
        # Если у вас есть роль "Admin", вместо непонятного <RoleOfUser object (1)> в админке вы увидите просто "Admin".


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен.')

        email = self.normalize_email(email)
        extra_fields.pop('username', None)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    # Django по умолчанию создает username, password, email.
    # Переопределяем их, чтобы они соответствовали схеме БД.
    id = None
    user_id = models.AutoField(primary_key=True, db_column='user_id', verbose_name='ID пользователя')
    username = None
    first_name = models.CharField(max_length=100, db_column='first_name', verbose_name='Имя')
    last_name = models.CharField(max_length=100, db_column='last_name', verbose_name='Фамилия')
    # email делаем обязательным и уникальным
    email = models.EmailField(
        unique=True, 
        db_column='email', 
        verbose_name='Электронная почта',
        error_messages={
            'unique': 'Пользователь с таким email уже существует.',
        }
    )
    phone = models.CharField(max_length=20, unique=True, db_column='phone', null=True, verbose_name='Телефон')
    # Используем стандартное password 
    registration_date = models.DateTimeField(auto_now_add=True, db_column='registration_date', verbose_name='Дата регистрации')
    
    # USERNAME_FIELD - поле, которое используется для аутентификации
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS - поля, обязательные при создании суперпользователя (кроме email и password)
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']
    objects = UserManager()

    # groups и permissions используются в админке Django. Использую их для технической логики
    # Для бизнес-логики буду использовать поле role, которое связано с таблицей role_of_user

    # Переопределяем группы с уникальным related_name
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # ← Уникальное имя!
        blank=True,
        verbose_name='Группы',
        help_text='The groups this user belongs to.'
    )
    
    # Переопределяем права с уникальным related_name
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # ← Уникальное имя!
        blank=True,
        verbose_name='Права пользователя',
        help_text='Specific permissions for this user.'
    )

    # Связь с ролью
    role = models.ForeignKey(
        RoleOfUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        db_column='role_of_user_role_id',
        verbose_name='Роль'
    )

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def is_manager(self):
        """Проверяет, менеджер ли пользователь"""
        return self.role is not None and self.role.role_name.lower() in ['менеджер']
    
    def is_customer(self):
        """Проверяет, клиент ли пользователь"""
        return self.role is not None and self.role.role_name.lower() in ['пользователь']


class DeliveryAddress(models.Model):
    address_id = models.AutoField(primary_key=True, db_column='address_id', verbose_name='ID адреса')
    city = models.CharField(max_length=100, db_column='city', verbose_name='Город')
    street = models.CharField(max_length=100, db_column='street', verbose_name='Улица')
    house = models.CharField(max_length=20, db_column='house', verbose_name='Дом')
    apartment = models.CharField(max_length=20, blank=True, null=True, db_column='apartment', verbose_name='Квартира')
    is_deleted = models.BooleanField(default=False, db_column='is_deleted', verbose_name='Удален')

    # Связь с пользователем
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_user_id', verbose_name='Пользователь')

    class Meta:
        db_table = 'delivery_address'
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'

    def __str__(self):
        return f"{self.city}, {self.street} {self.house}"
