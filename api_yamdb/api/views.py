from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Comment, Review


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    # permission_classes = доступно без токена/user,moderator,admin

    def get_queryset(self):
        """Получить отзыв по id для указанного произведения."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        """Добавление нового отзыва."""
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    # permission_classes = доступно без токена/user,moderator,admin

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
