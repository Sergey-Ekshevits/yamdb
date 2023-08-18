from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(Enum):
    user = 'Пользователь'
    moderator = 'Модератор'
    admin = 'Администратор'

    def get_all_roles():
        return [(role, role.value) for role in Roles]


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    email = models.EmailField(
        'E-mail пользователя',
        max_length=254,
        unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        choices=Roles.get_all_roles(),
        default=Roles.user,
        blank=False,
        max_length=50)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
