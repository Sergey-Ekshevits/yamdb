from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import CustomUser


class Review(models.Model):
    """Класс отзывов."""
    text = models.TextField('Текст отзыва', help_text='Отзыв')

    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='reviews')

    score = models.SmallIntegerField('Оценка',
                                     help_text='от 1 до 10',
                                     validators=[MinValueValidator(1),
                                                 MaxValueValidator(10)])

    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True,
                                    db_index=True)

    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Класс комментариев."""

    text = models.TextField('Текст комментария')

    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='comments')

    pub_date = models.DateTimeField('Дата добавления',
                                    auto_now_add=True, db_index=True)

    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
