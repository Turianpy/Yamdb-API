from django.core.validators import RegexValidator
from django.db import models

year_regex = RegexValidator(
    r'^\d{4}$',
    'Enter a valid year. The format should be YYYY.'
)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Title(models.Model):

    category = models.ManyToManyField(Category, related_name='titles')
    name = models.CharField(max_length=256)
    year = models.CharField(validators=[year_regex, ])
    description = models.CharField(required=False)

    def __str__(self) -> str:
        return f'{self.category.name} {self.name}, genre: {self.genre}'


class GenreTitle(models.Model):

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='titles')
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        related_name='genres')
