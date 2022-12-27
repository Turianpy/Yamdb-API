from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from api.models import Title
from reviews.models import Review
from reviews.serializers import (CommentSerializer,
                                 ReviewSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=request.user, title=title)

    def get_title(self):
        return get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = ()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('review_id')
        )
        serializer.save(author=request.user, review=review)

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()