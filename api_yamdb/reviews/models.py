from django.db import models


class CategoryGenreMixin(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(CategoryGenreMixin):
    pass


class Genre(CategoryGenreMixin):
    pass


class Title(models.Model):
    YEAR_CHOICES = [(year, year) for year in range(1895, 2023)]

    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(choices=YEAR_CHOICES)
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='genres')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='categories')

    def __str__(self):
        return self.name
