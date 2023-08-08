from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Comment, Review


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = PageNumberPagination

    # def get_queryset(self):
    #     post = get_object_or_404(Post, pk=self.kwargs["post_id"])
    #     return post.comments

    # def perform_create(self, serializer):
    #     post_id = self.kwargs.get('post_id')
    #     post = get_object_or_404(Post, id=post_id)
    #     serializer.save(author=self.request.user, post=post)
