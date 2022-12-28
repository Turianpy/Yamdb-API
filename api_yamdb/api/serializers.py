from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Genre, Review, Title


class TitleSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=True
    )
    rating = serializers.SerializerMethodField(read_only=True,)

    def get_rating(self, obj):
        ratings = Review.filter(title_id=obj.title_id)
        return ratings.aggregate(Avg('score'))['score__avg']

    class Meta:
        fields = '__all__'
        model = Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
