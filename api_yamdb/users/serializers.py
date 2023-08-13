import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from users.models import ROLES

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['username', 'email']


    def validate_username(self, value):
        if value.lower() == 'me' or not re.match("^[\w.@+-]+$", value):
            raise serializers.ValidationError('Некорректное имя пользователя')
        return value


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ['role']

    def validate_username(self, value):
        if value.lower() == 'me' or not re.match("^[\w.@+-]+$", value):
            raise serializers.ValidationError('Некорректное имя пользователя')
        return value


class UsersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150,
                                     required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(max_length=254,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    role = serializers.ChoiceField(required=False, default='user', choices=ROLES)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                message="Такой пользователь уже есть"
            ),
        ]

    def validate_username(self, value):
        if value.lower() == 'me' or not re.match("^[\w.@+-]+$", value):
            raise serializers.ValidationError('Некорректное имя пользователя')
        return value

    def validate_role(self, value):
        if value not in ('admin', 'user', 'moderator'):
            raise serializers.ValidationError('Некорректная роль пользователя')
        return value
