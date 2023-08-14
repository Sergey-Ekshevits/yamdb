from django.db.models import Avg, Q
from django.db.models.functions import Round
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .permissions import (
    AdminOrReadOnly, IsAuthorAdminModeratorOrReadOnly)
from .serializers import (
    CategorySerializer, GenreSerializer, TitleReadSerializer,
    TitleWriteSerializer, CommentSerializer, ReviewSerializer)
from reviews.models import Category, Genre, Title, Comment, Review


class AdminMixin:
    permission_classes = [AdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        slug = self.kwargs['pk']
        obj = queryset.get(slug=slug)
        self.check_object_permissions(self.request, obj)
        return obj


class CategoryViewSet(AdminMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'delete']


class GenreViewSet(AdminMixin, viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    http_method_names = ['get', 'post', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Round(Avg('reviews__score')))
    permission_classes = [AdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('year',)

    def get_queryset(self):
        queryset = self.queryset
        genre = self.request.query_params.get('genre')
        category = self.request.query_params.get('category')
        name = self.request.query_params.get('name')

        if genre:
            queryset = queryset.filter(
                Q(genre__name=genre) | Q(genre__slug=genre))
        if category:
            queryset = queryset.filter(
                category__slug=category)
        if name:
            queryset = queryset.filter(
                name__icontains=name)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorAdminModeratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorAdminModeratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
