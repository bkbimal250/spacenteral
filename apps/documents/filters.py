from django_filters import rest_framework as filters
from .models import Document, OwnerDocument, SpaManagerDocument


class DocumentFilter(filters.FilterSet):
    """Advanced filters for documents list"""

    created_from = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_to = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_from = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_to = filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    file_ext = filters.CharFilter(method='filter_file_ext')
    spa_code = filters.CharFilter(field_name='spa_code', lookup_expr='icontains')
    spa_name = filters.CharFilter(field_name='spa_name', lookup_expr='icontains')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    doc_type_name = filters.CharFilter(field_name='doc_type__name', lookup_expr='icontains')

    class Meta:
        model = Document
        fields = {
            'doc_type': ['exact'],
            'spa': ['exact'],
            'uploaded_by': ['exact'],
        }

    def filter_file_ext(self, queryset, name, value):
        """Filter by file extension: pdf, jpg, png, docx, etc."""
        if not value:
            return queryset
        value = value.lower().lstrip('.')
        return queryset.filter(file__iendswith=f'.{value}')


class OwnerDocumentFilter(filters.FilterSet):
    """Advanced filters for owner documents list"""

    created_from = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_to = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_from = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_to = filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    file_ext = filters.CharFilter(method='filter_file_ext')
    owner_name = filters.CharFilter(field_name='owner_name', lookup_expr='icontains')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = OwnerDocument
        fields = {
            'owner_type': ['exact'],
            'primary_owner': ['exact'],
            'secondary_owner': ['exact'],
            'third_owner': ['exact'],
            'fourth_owner': ['exact'],
            'uploaded_by': ['exact'],
        }

    def filter_file_ext(self, queryset, name, value):
        """Filter by file extension: pdf, jpg, png, docx, etc."""
        if not value:
            return queryset
        value = value.lower().lstrip('.')
        return queryset.filter(file__iendswith=f'.{value}')


class SpaManagerDocumentFilter(filters.FilterSet):
    """Advanced filters for spa manager documents list"""

    created_from = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_to = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_from = filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_to = filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    file_ext = filters.CharFilter(method='filter_file_ext')
    manager_name = filters.CharFilter(field_name='manager_name', lookup_expr='icontains')
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = SpaManagerDocument
        fields = {
            'spa_manager': ['exact'],
            'uploaded_by': ['exact'],
        }

    def filter_file_ext(self, queryset, name, value):
        """Filter by file extension: pdf, jpg, png, docx, etc."""
        if not value:
            return queryset
        value = value.lower().lstrip('.')
        return queryset.filter(file__iendswith=f'.{value}')

