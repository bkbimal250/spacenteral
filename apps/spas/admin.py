from django.contrib import admin
from .models import PrimaryOwner, SecondaryOwner, Spa


@admin.register(PrimaryOwner)
class PrimaryOwnerAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'email', 'phone', 'created_at']
    search_fields = ['fullname', 'email', 'phone']
    ordering = ['fullname']
    list_filter = ['created_at']


@admin.register(SecondaryOwner)
class SecondaryOwnerAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'email', 'phone', 'created_at']
    search_fields = ['fullname', 'email', 'phone']
    ordering = ['fullname']
    list_filter = ['created_at']


@admin.register(Spa)
class SpaAdmin(admin.ModelAdmin):
    list_display = [
        'spa_name', 'spa_code', 
        'primary_owner', 'secondary_owner', 
        'spamanager', 'status', 'agreement_status', 
        'area', 'created_at'
    ]
    list_filter = [
        'status', 'agreement_status',
        'area__city__state', 'area__city', 'area',
        'primary_owner', 'secondary_owner'
    ]
    search_fields = [
        'spa_name', 'spa_code', 
        'primary_owner__fullname', 'secondary_owner__fullname',
        'spamanager', 'emails', 'phones'
    ]
    raw_id_fields = ['primary_owner', 'secondary_owner', 'area', 'created_by']
    ordering = ['spa_name']
    fieldsets = (
        ('Basic Information', {
            'fields': ('spa_code', 'spa_name', 'status', 'spamanager')
        }),
        ('Ownership', {
            'fields': ('primary_owner', 'secondary_owner'),
            'description': 'Primary Owner is required. Secondary Owner is optional.'
        }),
        ('Location', {
            'fields': ('area', 'line_track', 'landmark', 'address', 'google_map_link')
        }),
        ('Contact Information', {
            'fields': ('emails', 'phones'),
            'description': 'Enter comma-separated values for multiple emails or phones.'
        }),
        ('Important Dates', {
            'fields': ('opening_date',)
        }),
        ('Agreement Details', {
            'fields': ('agreement_status', 'remark')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('primary_owner', 'secondary_owner', 'area__city__state')

# Register your models here.
