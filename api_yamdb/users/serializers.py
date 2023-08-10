from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import CustomUser

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def validate(self, attrs):
        if attrs['username'].lower() == 'me':
            raise serializers.ValidationError('Некорректное имя пользователя')
        return attrs


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
