from rest_framework import routers
from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

from users.views import UserCreateListViewset

from users.views import RegistrationAPIView, get_jwt_token, UserProfileAPI

router = routers.DefaultRouter()
#роутеры для работы с пользователями
# router.register('users/me', UserProfileViewSet, basename='users')
router.register(r'users', UserCreateListViewset)

router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

# router.register(r'auth/token', RegistrationAPIView.as_view(), basename='token')
# router.register(r'auth/signup', get_jwt_token, basename='signup')

urlpatterns = [
    # пока так некрасиво, но работает. В роутеры если так добавлять выдает ошибку
    path('v1/auth/signup/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', get_jwt_token, name='token_obtain_pair'),
    # Это тоже не совсем красиво, но вьюсеты отдают отдают лишние параметры в url
    path('v1/users/me/', UserProfileAPI.as_view()),
    path('v1/', include(router.urls)),
]

