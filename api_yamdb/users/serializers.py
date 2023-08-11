from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import CustomUser

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def create(self, validated_data):
        obj, result = CustomUser.objects.get_or_create(**validated_data)
        print(result)
        return obj


class ConfirmationCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        # read_only_fields = ['role']

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request", None)
        if request and request.user.is_staff and request.user.is_superuser is False:
            fields['role'].read_only = True
        return fields