from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import CustomUser
import re


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    # username = serializers.RegexField(r"^[\w.@+-]+\z")
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ['username', 'email']

    # validators = [
    #     UniqueTogetherValidator(
    #         queryset=User.objects.all(),
    #         fields=('username', 'email'),
    #         message="Такой пользователь уже есть"
    #     )
    # ]

    def create(self, validated_data):
        obj, result = CustomUser.objects.get_or_create(**validated_data)
        print(result)
        return obj

    def validate_username(self, value):
        if value.lower() == 'me' or not re.match("^[\w.@+-]+$", value):
            raise serializers.ValidationError('Некорректное имя пользователя')
        return value




class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()


class UsersSerializer(serializers.ModelSerializer):
    # username = serializers.RegexField(r"^[\w.@+-]+\z")
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     http_method = self.context['request'].method
    #
    #     if http_method in ['POST', 'PATCH']:
    #         self.fields['email'].required = True
    #     else:
    #         self.fields['email'].required = False

    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    # password = serializers.CharField(max_length=254, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        read_only_fields = ['role']
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email'),
                message="Такой пользователь уже есть"
            )
        ]

    # def get_fields(self):
    #     fields = super().get_fields()
    #     request = self.context.get("request", None)
    #     if request and request.user.is_staff and request.user.is_superuser is False:
    #         fields['role'].read_only = True
    #     return fields

    def validate_username(self, value):
        if value.lower() == 'me' or not re.match("^[\w.@+-]+$", value):
            raise serializers.ValidationError('Некорректное имя пользователя')
        return value
