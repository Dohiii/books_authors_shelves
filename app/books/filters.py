from django_filters import rest_framework as filters
from .models import Book


class BooksFilter(filters.FilterSet):
    author = filters.CharFilter(field_name="authors",
                                lookup_expr='icontains')
    from_ = filters.NumberFilter(field_name="published_year",
                                 lookup_expr='gte')
    to = filters.NumberFilter(field_name="published_year",
                              lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['authors', 'published_year', 'acquired']
