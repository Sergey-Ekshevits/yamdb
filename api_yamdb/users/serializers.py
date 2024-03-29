import re

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import Roles

User = get_user_model()


class UserSerializerMixin(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    def validate_username(self, value):
        if value.lower() == 'me' or not re.match(r"^[\w.@+-]+$", value):
            raise serializers.ValidationError('Некорректное имя пользователя')
        return value

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')


class RegistrationSerializer(UserSerializerMixin, serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email')


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()


class UserProfileSerializer(UserSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        read_only_fields = ('role',)


class UsersSerializer(UserSerializerMixin, serializers.ModelSerializer):
    role = serializers.ChoiceField(required=False,
                                   default='user',
                                   choices=[role.name for role in Roles])
