from rest_framework import routers
from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

from users.views import UserListViewset

from users.views import RegistrationAPIView, get_jwt_token

router = routers.DefaultRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

#роутеры для работы с пользователями
router.register(r'users', UserListViewset)

urlpatterns = [
    path('v1/', include(router.urls)),
    # пока так некрасиво, но работает. В роутеры если так добавлять выдает ошибку
    path('v1/auth/signup/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', get_jwt_token, name='token_obtain_pair')
]
