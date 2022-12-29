from django.db.models import Avg
from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Review, Title
from users.models import User
from .validators import validate_email, validate_username


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


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, allow_blank=False,
                                   validators=[validate_email])
    username = serializers.CharField(max_length=150, allow_blank=False,
                                     validators=[validate_username])

    class Meta:
        model = User
        fields = ('email', 'username')


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    confirmation_code = serializers.CharField(
        required=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = default_token_generator.make_token(user)
        if str(confirmation_code) != data['confirmation_code']:
            raise ValidationError('Неверный код подтверждения')
        return data
