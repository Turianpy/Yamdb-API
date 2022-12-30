from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title
from users.models import User

from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          GetTokenSerializer, SignUpSerializer,
                          TitleSerializer, TitleSerializerWithSlugFields,
                          UserSerializer)
from .viewsets import CreateListDelVS
from .filters import TitleFilter


class TitleViewSet(viewsets.ModelViewSet):

    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitleSerializerWithSlugFields


class GenreViewSet(CreateListDelVS):

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDelVS):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_confirmation_code(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    if not User.objects.filter(email=email).exists():
        User.objects.create(
            username=username, email=email
        )
    user = User.objects.filter(email=email).first()
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Код подтверждения Yamdb',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    return Response(
        serializer.validated_data,
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
    print(serializer.is_valid())
    user = get_object_or_404(User, username=request.data['username'])
    print('got user')
    confirmation_code = request.data['confirmation_code']
    print('got conf code')
    print(default_token_generator.check_token(user, confirmation_code))
    if default_token_generator.check_token(user, confirmation_code):
        token = get_tokens_for_user(user)
        print(token)
        response = {'token': str(token['access'])}
        return Response(response, status=status.HTTP_200_OK)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrReadOnly, permissions.IsAuthenticated)
    lookup_field = 'username'

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def me(self, request, pk=None):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == "PATCH":
            if 'role' in request.data and not (user.is_admin or user.is_staff):
                return Response(
                    {"Naughty boy"},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
