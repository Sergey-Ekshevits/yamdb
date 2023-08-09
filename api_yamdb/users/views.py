from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ConfirmationCodeSerializer, RegistrationSerializer
from .utils import send_verification_mail, confirmation_code_generator

User = get_user_model()

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        user_email = request.data.get('email')
        generated_code = confirmation_code_generator()
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save(confirmation_code=generated_code)
        send_verification_mail(user_email, generated_code)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
            return Response({'token': access_token}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid confirmation code'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

