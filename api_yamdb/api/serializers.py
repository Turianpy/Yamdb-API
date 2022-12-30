from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .validators import validate_email, validate_username


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ['id']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['id']


class TitleSerializer(serializers.ModelSerializer):

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField(read_only=True,)

    def get_rating(self, obj):
        ratings = Review.objects.filter(title_id=obj.id)
        return ratings.aggregate(Avg('score'))['score__avg']

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializerWithSlugFields(TitleSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug',
        queryset=Genre.objects.all()
    )


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
        if data['confirmation_code'] != user.confirmation_code:
            raise ValidationError('Неверный код подтверждения')
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role'
        ]
