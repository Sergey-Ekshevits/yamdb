from rest_framework import routers
from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

from users.views import UserListViewset

router = routers.DefaultRouter()

router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)

#роутеры для работы с пользователями
router.register(r'users', UserListViewset)

urlpatterns = [
    path('v1/', include(router.urls)),
]
