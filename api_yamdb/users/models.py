from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class CustomUser(AbstractUser):
    """Кастомная модель пользователя."""
    username = models.CharField('Имя пользователя',
                                max_length=150,
                                unique=True
                                )
    email = models.EmailField(
        'E-mail пользователя',
        max_length=254,
        unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль',
        choices=ROLES,
        default='user',
        blank=False,
        max_length=50)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
