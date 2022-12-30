from datetime import datetime

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Avg
from rest_framework.validators import ValidationError
from users.models import User

year_regex = RegexValidator(
    r'^\d{4}$',
    'Enter a valid year. The format should be YYYY.'
)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']


class Title(models.Model):
    category = models.ForeignKey(
        Category, related_name='titles',
        on_delete=models.SET_NULL, null=True
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(validators=[year_regex, ])
    description = models.CharField(max_length=1000)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)

    @property
    def get_rating(self):
        ratings = self.reviews.all()
        return ratings.aggregate(Avg('score'))['score__avg']

    def save(self, *args, **kwargs):
        self.rating = self.get_rating
        return super(Title, self).save(*args, **kwargs)

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


class Review(models.Model):
    def validate_interval(value):
        if not 10 >= value >= 1:
            raise ValidationError(
                ('%(value)s Score must be between 0 and 10.'),
                params={'value': value},
            )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.IntegerField(validators=[validate_interval])
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return f'{self.title}, {self.author}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='сomments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='сomments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text
