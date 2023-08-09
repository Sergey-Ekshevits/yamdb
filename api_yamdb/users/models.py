from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, **extra_fields):
        if not email:
            raise ValueError("E-mail обязательное поле")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField('Имя пользователя', max_length=150, unique=True)
    email = models.EmailField('E-mail пользователя', max_length=254, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль',
                            choices=ROLES,
                            default='user',
                            blank=False,
                            max_length=25)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField('Имя', max_length=150, null=True)
    last_name = models.CharField('Фамилия', max_length=150, null=True)
    confirmation_code = models.CharField(null=True, max_length=25)
    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']
