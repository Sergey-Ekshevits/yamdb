from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class CustomUser(AbstractUser):
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль',
                            choices=ROLES,
                            default='user',
                            blank=False,
                            max_length=25)
