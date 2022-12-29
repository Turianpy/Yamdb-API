from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .viewsets import CreateListDelVS
from .serializers import SignUpSerializer, GetTokenSerializer
from users.models import User


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


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_confirmation_code(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    if not User.objects.filter(email=email).exists():
        User.objects.create(
            username=email, email=email
        )
    user = User.objects.filter(email=email).first()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения Yamdb',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    return Response(
        {'result': 'Код подтверждения успешно отправлен!'},
        status=status.HTTP_200_OK
    )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    confirmation_code = request.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = get_tokens_for_user(user)
        response = {'token': str(token['access'])}
        return Response(response, status=status.HTTP_200_OK)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
