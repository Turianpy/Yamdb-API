from django_filters import rest_framework as f
from reviews.models import Title


class TitleFilter(f.FilterSet):
    category = f.CharFilter(
        field_name='category__slug', lookup_expr='icontains'
    )
    genre = f.CharFilter(
        field_name='genre__slug', lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
