from django_filters import rest_framework as filters
from .models import Document


class DocumentFilter(filters.FilterSet):
    """Advanced filters for documents list"""

    created_from = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_to = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_from = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_to = filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    file_ext = filters.CharFilter(method='filter_file_ext')

    class Meta:
        model = Document
        fields = {
            'user': ['exact'],
            'doc_type': ['exact'],
            'uploaded_by': ['exact'],
        }

    def filter_file_ext(self, queryset, name, value):
        """Filter by file extension: pdf, jpg, png, docx, etc."""
        if not value:
            return queryset
        value = value.lower().lstrip('.')
        return queryset.filter(file__iendswith=f'.{value}')


