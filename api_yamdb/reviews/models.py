from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,related_name='reviwes'
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='author'
    )
    text = models.TextField('Текст', help_text='Отзыв')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.SmallIntegerField('Оценка',
                                     validators=[MinValueValidator(1),
                                                 MaxValueValidator(10)])

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='author'
    )
    title = models.ForeignKey('Комментарий',
                              Review, on_delete=models.CASCADE,
                              related_name='comments',
                              help_text="Ваш комментарий")

    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
