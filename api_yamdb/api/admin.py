from django.contrib import admin
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

admin.site.register(
    [Title, Genre, GenreTitle, Category, Review, Comment]
)
