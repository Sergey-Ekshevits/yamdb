from rest_framework import routers
from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet, TitleViewSet, CommentViewSet, ReviewViewSet

from users.views import RegistrationAPIView, get_jwt_token, UserProfileAPI, UsersViewset

router = routers.DefaultRouter()
#роутеры для работы с пользователями
router.register(r'users', UsersViewset)

router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews', ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [
    # пока так некрасиво, но работает. В роутеры если так добавлять выдает ошибку
    path('v1/auth/signup/', RegistrationAPIView.as_view()),
    path('v1/auth/token/', get_jwt_token, name='token_obtain'),
    path('v1/users/me/', UserProfileAPI.as_view()),
    path('v1/', include(router.urls)),
]
