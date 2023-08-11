from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, filters, mixins
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ConfirmationCodeSerializer, RegistrationSerializer, UsersSerializer
from .utils import send_verification_mail, confirmation_code_generator
from .permissions import IsOwner

User = get_user_model()


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data
        user_email = request.data.get('email')
        generated_code = confirmation_code_generator()
        serializer = self.serializer_class(data=user)
        existing_user = User.objects.filter(email=user_email).first()
        send_verification_mail(user_email, generated_code)
        if not existing_user:
            serializer.is_valid(raise_exception=True)
            serializer.save(confirmation_code=generated_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            existing_user.confirmation_code = generated_code
            existing_user.save()
#Это безобразие, но пока так
        return Response("success", status=status.HTTP_201_CREATED)


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


class CreateListViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


# Не сработало

# class RetrieveUpdateViewSet(mixins.RetrieveModelMixin,
#                         mixins.UpdateModelMixin,
#                         viewsets.GenericViewSet):
#     pass
#
#
# class UserProfileViewSet(RetrieveUpdateViewSet):
#     queryset = User.objects.all()
#     serializer_class = UsersSerializer
#     permission_classes = [IsOwner]
#
#     # def get_queryset(self):
#     #     current_user = self.request.user
#     #     return User.objects.filter(user=current_user.id)



class UserProfileAPI(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        user = request.user
        serializer = UsersSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = UsersSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreateListViewset(CreateListViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = (IsAdminUser,)
    search_fields = ['username']

    def perform_create(self, serializer):
        user = serializer.save()
        if user.role == 'admin':
            user.is_staff = True
        user.save()


class UsersViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]
