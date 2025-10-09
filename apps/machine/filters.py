from django_filters import rest_framework as filters
from .models import Machine, AccountHolder


class MachineFilter(filters.FilterSet):
    """Comprehensive filter for machines"""
    serial = filters.CharFilter(field_name='serial_number', lookup_expr='icontains')
    machine_code = filters.CharFilter(field_name='machine_code', lookup_expr='icontains')
    machine_name = filters.CharFilter(field_name='machine_name', lookup_expr='icontains')
    model = filters.CharFilter(field_name='model_name', lookup_expr='icontains')
    
    # Location filters (through spa's location)
    state = filters.NumberFilter(field_name='spa__area__city__state__id')
    city = filters.NumberFilter(field_name='spa__area__city__id')
    area = filters.NumberFilter(field_name='spa__area__id')
    spa = filters.NumberFilter(field_name='spa__id')
    spa_landmark = filters.CharFilter(field_name='spa__landmark', lookup_expr='icontains')
    
    # Status filter
    status = filters.ChoiceFilter(choices=Machine.STATUS_CHOICES)
    
    # Banking filters
    mid = filters.CharFilter(field_name='mid', lookup_expr='icontains')
    tid = filters.CharFilter(field_name='tid', lookup_expr='icontains')
    bank_name = filters.CharFilter(field_name='bank_name', lookup_expr='icontains')
    account_name = filters.CharFilter(field_name='account_name', lookup_expr='icontains')
    
    # Account holder filters
    acc_holder = filters.NumberFilter(field_name='acc_holder__id')
    acc_holder_name = filters.CharFilter(field_name='acc_holder__full_name', lookup_expr='icontains')
    acc_holder_designation = filters.CharFilter(field_name='acc_holder__designation', lookup_expr='icontains')

    class Meta:
        model = Machine
        fields = [
            'serial', 'machine_code', 'machine_name', 'model',
            'state', 'city', 'area', 'spa', 'spa_landmark', 'status',
            'mid', 'tid', 'bank_name', 'account_name',
            'acc_holder', 'acc_holder_name', 'acc_holder_designation'
        ]

