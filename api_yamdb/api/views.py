from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .viewsets import CreateListDelVS


class TitleViewSet(viewsets.ModelViewSet):

    serializer_class = TitleSerializer
    queryset = Title.objects.all()

    permission_classes = []


class GenreViewSet(CreateListDelVS):

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    permission_classes = []


class CategoryViewSet(CreateListDelVS):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    permission_classes = []
