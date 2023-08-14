from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from .serializers import (ConfirmationCodeSerializer, RegistrationSerializer,
                          UserProfileSerializer, UsersSerializer)
from .utils import confirmation_code_generator, send_verification_mail

User = get_user_model()


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        user_email = request.data.get('email')
        username = request.data.get('username')
        generated_code = confirmation_code_generator()
        serializer = self.serializer_class(data=user)
        existing_user = User.objects.filter(email=user_email,
                                            username=username).first()
        send_verification_mail(user_email, generated_code)
        if not existing_user:
            serializer.is_valid(raise_exception=True)
            try:
                serializer.save(confirmation_code=generated_code)
            except IntegrityError:
                return Response("bad request",
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        elif (existing_user.username,
              existing_user.email) != (username,
                                       user_email):
            return Response("Такой пользователь уже есть",
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            existing_user.confirmation_code = generated_code
            existing_user.save()
        return Response("Сообщение с кодом отправлено",
                        status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if confirmation_code == user.confirmation_code:
            user = get_object_or_404(User, username=username)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({'token': access_token},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Неверный код'},
                            status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPI(APIView):
    permission_classes = (IsAuthenticated,)
    serializers_class = UserProfileSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializers_class(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = self.serializers_class(user,
                                            data=request.data,
                                            partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ('patch', 'get', 'delete', 'post')
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    search_fields = ['username']

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user.role == 'admin':
            user.is_staff = True
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        if user.role == 'admin':
            user.is_staff = True
        else:
            user.is_staff = False
        user.save()
