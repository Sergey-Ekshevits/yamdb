# Generated by Django 3.2 on 2023-08-13 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20230812_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Аутентифицированный пользователь', 'User'), ('Модератор', 'Moderator'), ('Администратор', 'Admin')], default='user', max_length=50, verbose_name='Роль'),
        ),
    ]
