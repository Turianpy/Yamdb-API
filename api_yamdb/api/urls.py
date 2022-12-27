from django.urls import include, path
from rest_framework import routers

from . import views

v1_router = routers.DefaultRouter()
v1_router.register('titles', views.TitleViewSet, basename='titles')
v1_router.register('categories', views.CategoryViewSet, basename='categories')
v1_router.register('genres', views.GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
