from django.core.validators import RegexValidator
from django.db import models
from datetime import datetime
from rest_framework.validators import ValidationError

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

    category = models.ForeignKey(
        Category, related_name='titles',
        on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(validators=[year_regex, ])
    description = models.CharField()

    def __str__(self) -> str:
        return f'{self.category.name} {self.name}'

    def clean(self):
        if self.year > datetime.now().year:
            raise ValidationError("Has to be current or past year.")
        return super().clean()


class GenreTitle(models.Model):

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='genres')
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE,
        related_name='titles')
