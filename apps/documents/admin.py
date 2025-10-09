from django.contrib import admin
from .models import DocumentType, Document


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'doc_type', 'spa_display', 'uploaded_by', 'created_at']
    list_filter = ['doc_type', 'uploaded_by', 'created_at', 'spa__area__city__state']
    search_fields = ['title', 'spa_code', 'spa_name', 'notes']
    raw_id_fields = ['spa', 'uploaded_by']
    ordering = ['-created_at']
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'doc_type', 'file', 'notes')
        }),
        ('Spa Assignment', {
            'fields': ('spa',),
            'description': 'Select the spa this document belongs to. Location info will be auto-populated.'
        }),
        ('Legacy User Fields (Optional)', {
            'fields': ('user', 'users'),
            'description': 'Legacy user assignment fields (kept for backward compatibility).',
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['uploaded_by', 'created_at', 'updated_at']
    
    def spa_display(self, obj):
        """Display spa information"""
        if obj.spa:
            return f"{obj.spa_code} - {obj.spa_name}"
        return "-"
    spa_display.short_description = 'Spa'

# Register your models here.
