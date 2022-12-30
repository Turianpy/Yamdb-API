from rest_framework import serializers
from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        author = self.context['request'].user
        if not self.context['request'].method == 'PATCH':
            if Review.objects.filter(title__id=title_id,
                                     author=author).exists():
                raise serializers.ValidationError(
                    'You can write only one review!'
                )
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
