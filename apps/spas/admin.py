from django.contrib import admin
from django.utils.html import format_html
from .models import PrimaryOwner, SecondaryOwner, ThirdOwner, FourthOwner, Spa, SpaManager


# Import for inline
class SpaManagerDocumentInline(admin.TabularInline):
    """Inline for managing documents within SpaManager admin"""
    from apps.documents.models import SpaManagerDocument
    model = SpaManagerDocument
    extra = 0
    fields = ['title', 'file', 'notes', 'created_at']
    readonly_fields = ['created_at']
    verbose_name = 'Document'
    verbose_name_plural = 'Manager Documents'
    can_delete = True
    show_change_link = True


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


@admin.register(ThirdOwner)
class ThirdOwnerAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'email', 'phone', 'created_at']
    search_fields = ['fullname', 'email', 'phone']
    ordering = ['fullname']
    list_filter = ['created_at']


@admin.register(FourthOwner)
class FourthOwnerAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'email', 'phone', 'created_at']
    search_fields = ['fullname', 'email', 'phone']
    ordering = ['fullname']
    list_filter = ['created_at']


@admin.register(Spa)
class SpaAdmin(admin.ModelAdmin):
    list_display = [
        'spa_name', 'spa_code', 
        'primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner',
        'spamanager', 'status', 'agreement_status', 
        'area', 'created_at'
    ]
    list_filter = [
        'status', 'agreement_status',
        'area__city__state', 'area__city', 'area',
        'primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner'
    ]
    search_fields = [
        'spa_name', 'spa_code', 
        'primary_owner__fullname', 'secondary_owner__fullname',
        'third_owner__fullname', 'fourth_owner__fullname',
        'spamanager', 'emails', 'phones'
    ]
    raw_id_fields = ['primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner', 'area', 'created_by']
    ordering = ['spa_name']
    fieldsets = (
        ('Basic Information', {
            'fields': ('spa_code', 'spa_name', 'status', 'spamanager')
        }),
        ('Ownership', {
            'fields': ('primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner'),
            'description': 'Primary Owner is required. Secondary, Third, and Fourth Owners are optional.'
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
        return qs.select_related('primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner', 'area__city__state')


@admin.register(SpaManager)
class SpaManagerAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'email_display', 'phone_display', 'spa_display', 'document_count', 'created_at']
    search_fields = ['fullname', 'email', 'phone', 'spa__spa_name', 'spa__spa_code']
    list_filter = ['created_at', 'spa']
    raw_id_fields = ['spa']
    ordering = ['fullname']
    list_per_page = 25
    date_hierarchy = 'created_at'
    inlines = [SpaManagerDocumentInline]
    
    fieldsets = (
        ('Manager Information', {
            'fields': ('fullname', 'email', 'phone', 'address')
        }),
        ('Spa Assignment', {
            'fields': ('spa',),
            'description': 'Select the spa this manager belongs to (optional).'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    actions = ['assign_to_spa']
    
    def spa_display(self, obj):
        """Display spa information with link"""
        if obj.spa:
            return format_html(
                '<a href="/admin/spas/spa/{}/change/">{} - {}</a>',
                obj.spa.id,
                obj.spa.spa_code,
                obj.spa.spa_name
            )
        return format_html('<span style="color: #999;">Not Assigned</span>')
    spa_display.short_description = 'Spa'
    
    def email_display(self, obj):
        """Display email with mailto link"""
        if obj.email:
            return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)
        return '-'
    email_display.short_description = 'Email'
    
    def phone_display(self, obj):
        """Display phone with tel link"""
        if obj.phone:
            return format_html('<a href="tel:{}">{}</a>', obj.phone, obj.phone)
        return '-'
    phone_display.short_description = 'Phone'
    
    def document_count(self, obj):
        """Display number of documents"""
        count = obj.documents.count()
        if count > 0:
            return format_html(
                '<a href="/admin/documents/spamanagerdocument/?spa_manager__id__exact={}">{} docs</a>',
                obj.id,
                count
            )
        return '0 docs'
    document_count.short_description = 'Documents'
    
    def assign_to_spa(self, request, queryset):
        """Bulk action to assign managers to a spa"""
        # This would need a custom form, but we'll add it as a placeholder
        self.message_user(request, f"{queryset.count()} managers selected. Use individual edit to assign to spa.")
    assign_to_spa.short_description = "Assign selected managers to spa"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('spa').prefetch_related('documents')

# Register your models here.
