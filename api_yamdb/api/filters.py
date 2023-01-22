from django_filters import CharFilter, FilterSet

from reviews.models import Title


class SlugFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug', lookup_expr='contains')
    category = CharFilter(field_name='category__slug', lookup_expr='contains')
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('genre', 'name', 'year', 'category',)
