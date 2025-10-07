from django_filters import rest_framework as filters
from .models import Machine


class MachineFilter(filters.FilterSet):
    serial = filters.CharFilter(field_name='serial_number', lookup_expr='icontains')
    state = filters.NumberFilter(field_name='installed_area.city.state_id')
    city = filters.NumberFilter(field_name='installed_area.city_id')
    area = filters.NumberFilter(field_name='installed_area_id')
    status = filters.CharFilter(field_name='status')
    spa = filters.NumberFilter(field_name='spa_id')

    class Meta:
        model = Machine
        fields = ['serial', 'state', 'city', 'area', 'status', 'spa']

