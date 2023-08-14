from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class CustomUser(AbstractUser):
    username = models.CharField('Имя пользователя',
                                max_length=150,
                                unique=True
                                )
    email = models.EmailField('E-mail пользователя',
                              max_length=254,
                              unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль',
                            choices=ROLES,
                            default='user',
                            blank=False,
                            max_length=50)
    first_name = models.CharField('Имя', max_length=150, null=True, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, null=True, blank=True)
    confirmation_code = models.CharField(null=True, max_length=25)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]
