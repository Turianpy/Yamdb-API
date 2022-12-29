from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import EmailMessage

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .viewsets import CreateListDelVS
from .serializers import SignUpSerializer


class TitleViewSet(viewsets.ModelViewSet):

    serializer_class = TitleSerializer
    queryset = Title.objects.all()

    permission_classes = []
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')


class GenreViewSet(CreateListDelVS):

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    permission_classes = []
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDelVS):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    permission_classes = []
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class APISignup(APIView):
    """
    Получить код подтверждения на переданный email.
    Для любого пользователя
    """
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            'Ваш код подтверждения для доступа к API: {12345}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтверждения для доступа к API'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
