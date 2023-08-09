from django.urls import include, path
from rest_framework import routers


from .views import CommentViewSet, ReviewViewSet

router = routers.DefaultRouter()


router.register(
    r'titles/(?P<title_id>[^/.]+)/reviews', ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>[^/.])/reviews/(?P<review_id>[^/.])/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
