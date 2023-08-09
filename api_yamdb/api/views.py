from rest_framework import filters, viewsets

from .serializers import (
    CategorySerializer, GenreSerializer, TitleReadSerializer,
    TitleWriteSerializer)
from reviews.models import Category, Genre, Title


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    # Поиск чувствителен только к регистру букв на кириллице.
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']
    # DELETE запрос доработать. Удаление по id в эндпоинте, нужно по slug.
    # К GenreViewSet то же.


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    # Response в POST запросах отличается от документации.
    # В GET запросах всё как надо.
    queryset = Title.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer
