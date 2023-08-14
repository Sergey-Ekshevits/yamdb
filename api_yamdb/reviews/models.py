import datetime

from django.db import models
from django.db.models import UniqueConstraint

from users.models import CustomUser


class CategoryGenreMixin(models.Model):
    """
    Абстрактная модель для моделей Category и Genre.
    Содержит поля name и slug.
    """
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг', max_length=50, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Category(CategoryGenreMixin):
    """Модель категорий произведений."""

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryGenreMixin):
    """Модель жанров произведений."""

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведений."""
    current_year = datetime.datetime.now().year
    YEAR_CHOICES = [(year, year) for year in range(1895, current_year + 1)]

    name = models.CharField('Название', max_length=256)
    year = models.PositiveIntegerField('Год выпуска', choices=YEAR_CHOICES)
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
        verbose_name='жанр')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='categories',
        verbose_name='категория')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов."""
    CHOICES = [(score, score) for score in range(1, 11)]

    text = models.TextField('Текст отзыва')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор')
    score = models.SmallIntegerField(
        'Оценка',
        help_text='от 1 до 10',
        choices=CHOICES)
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев."""
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв')

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
