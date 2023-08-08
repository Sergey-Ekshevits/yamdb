from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User
from reviews.models import Title


class Review(models.Model):
    """Класс отзывов."""
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviwes',
                              verbose_name='Произведение',)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author')
    text = models.TextField('Текст отзыва', help_text='Отзыв')
    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)
    score = models.SmallIntegerField('Оценка',
                                     help_text='от 0 до 10',
                                     validators=[MinValueValidator(1),
                                                 MaxValueValidator(10)])

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Класс комментариев."""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               help_text='Ваш комментарий')

    text = models.TextField(verbose_name='текст')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
