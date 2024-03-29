# Generated by Django 3.2 on 2023-08-16 15:27

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[(users.models.Roles['user'], 'Пользователь'), (users.models.Roles['moderator'], 'Модератор'), (users.models.Roles['admin'], 'Администратор')], default=users.models.Roles['user'], max_length=50, verbose_name='Роль'),
        ),
    ]
