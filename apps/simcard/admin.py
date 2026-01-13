from django.contrib import admin
from django.utils.html import format_html
from .models import SimCard


@admin.register(SimCard)
class SimCardAdmin(admin.ModelAdmin):
    list_display = [
        'mobile_number', 'simcard_serial_number', 'sim_owner_name',
        'spa_display', 'status', 'date_of_issue', 'created_at'
    ]
    list_filter = [
        'status', 'date_of_issue', 'created_at', 'spa'
    ]
    search_fields = [
        'mobile_number', 'simcard_serial_number', 'sim_owner_name',
        'spa__spa_name', 'spa__spa_code'
    ]
    raw_id_fields = ['spa', 'created_by', 'updated_by']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('SimCard Information', {
            'fields': (
                'mobile_number', 'simcard_serial_number', 'sim_owner_name',
                'date_of_issue', 'status'
            )
        }),
        ('Spa Assignment', {
            'fields': ('spa',),
            'description': 'Select the spa this simcard belongs to (optional).'
        }),
        ('Metadata', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def spa_display(self, obj):
        """Display spa information with link"""
        if obj.spa:
            return format_html(
                '<a href="/admin-panel/dishaonlinesolution/spas/spa/{}/change/">{} - {}</a>',
                obj.spa.id,
                obj.spa.spa_code,
                obj.spa.spa_name
            )
        return format_html('<span style="color: #999;">Not Assigned</span>')
    spa_display.short_description = 'Spa'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'spa', 'spa__area', 'spa__area__city', 'spa__area__city__state',
            'created_by', 'updated_by'
        )
