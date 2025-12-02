import django_filters
from .models import Spa, PrimaryOwner, SecondaryOwner, ThirdOwner, FourthOwner, SpaManager, SocialMediaLink,SpaWebsite


class SpaFilter(django_filters.FilterSet):
    """Advanced filters for Spa model"""
    
    # Text search
    spa_name = django_filters.CharFilter(lookup_expr='icontains')
    spa_code = django_filters.CharFilter(lookup_expr='icontains')
    spamanager = django_filters.CharFilter(lookup_expr='icontains')
    
    # Status filters
    status = django_filters.ChoiceFilter(choices=Spa.STATUS_CHOICES)
    agreement_status = django_filters.ChoiceFilter(choices=Spa.AGREEMENT_STATUS_CHOICES)
    
    # Owner filters
    primary_owner = django_filters.ModelChoiceFilter(queryset=PrimaryOwner.objects.all())
    secondary_owner = django_filters.ModelChoiceFilter(queryset=SecondaryOwner.objects.all())
    third_owner = django_filters.ModelChoiceFilter(queryset=ThirdOwner.objects.all())
    fourth_owner = django_filters.ModelChoiceFilter(queryset=FourthOwner.objects.all())
    
    # Location filters
    state = django_filters.NumberFilter(field_name='area__city__state')
    city = django_filters.NumberFilter(field_name='area__city')
    area = django_filters.NumberFilter(field_name='area')
    
    # Date filters
    opening_date_from = django_filters.DateFilter(field_name='opening_date', lookup_expr='gte')
    opening_date_to = django_filters.DateFilter(field_name='opening_date', lookup_expr='lte')
    
    # Created date filters
    created_from = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_to = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Spa
        fields = [
            'spa_name', 'spa_code', 'spamanager', 'status', 'agreement_status',
            'primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner', 'state', 'city', 'area'
        ]


class PrimaryOwnerFilter(django_filters.FilterSet):
    """Filters for PrimaryOwner model"""
    
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = PrimaryOwner
        fields = ['fullname', 'email', 'phone']


class SecondaryOwnerFilter(django_filters.FilterSet):
    """Filters for SecondaryOwner model"""
    
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = SecondaryOwner
        fields = ['fullname', 'email', 'phone']


class ThirdOwnerFilter(django_filters.FilterSet):
    """Filters for ThirdOwner model"""
    
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = ThirdOwner
        fields = ['fullname', 'email', 'phone']


class FourthOwnerFilter(django_filters.FilterSet):
    """Filters for FourthOwner model"""
    
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = FourthOwner
        fields = ['fullname', 'email', 'phone']


class SpaManagerFilter(django_filters.FilterSet):
    """Filters for SpaManager model"""
    
    fullname = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    spa = django_filters.ModelChoiceFilter(queryset=Spa.objects.all())
    
    class Meta:
        model = SpaManager
        fields = ['fullname', 'email', 'phone', 'spa']


class SocialMediaLinkFilter(django_filters.FilterSet):
    """Filters for SocialMediaLink model"""

    platform = django_filters.CharFilter(lookup_expr='icontains')
    spa = django_filters.ModelChoiceFilter(queryset=Spa.objects.all())

    class Meta:
        model = SocialMediaLink
        fields = ['platform', 'spa']


class SpaWebsiteFilter(django_filters.FilterSet):
    """Filters for SpaWebsite model"""

    url = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')
    spa = django_filters.ModelChoiceFilter(queryset=Spa.objects.all())

    class Meta:
        model = SpaWebsite
        fields = ['url', 'spa','category']

