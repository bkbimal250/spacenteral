from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import DocumentType, Document, OwnerDocument, SpaManagerDocument


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


@admin.register(OwnerDocument)
class OwnerDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner_display', 'owner_type', 'uploaded_by', 'created_at']
    list_filter = ['owner_type', 'uploaded_by', 'created_at']
    search_fields = ['title', 'owner_name', 'notes']
    raw_id_fields = ['primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner', 'uploaded_by']
    ordering = ['-created_at']
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'file', 'notes')
        }),
        ('Owner Assignment (Select Only ONE)', {
            'fields': ('primary_owner', 'secondary_owner', 'third_owner', 'fourth_owner'),
            'description': 'Select ONLY ONE owner for this document. The system will validate this.'
        }),
        ('Metadata (Auto-populated)', {
            'fields': ('owner_name', 'owner_type', 'uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['owner_name', 'owner_type', 'uploaded_by', 'created_at', 'updated_at']
    
    def owner_display(self, obj):
        """Display owner name"""
        return obj.owner_name or "-"
    owner_display.short_description = 'Owner'


@admin.register(SpaManagerDocument)
class SpaManagerDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'file_preview', 'manager_display', 'spa_display', 'file_size_display', 'uploaded_by', 'created_at']
    list_filter = ['uploaded_by', 'created_at', 'spa_manager']
    search_fields = ['title', 'manager_name', 'notes', 'spa_manager__fullname']
    raw_id_fields = ['spa_manager', 'uploaded_by']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'file', 'file_preview_detail', 'notes')
        }),
        ('Manager Assignment', {
            'fields': ('spa_manager',),
            'description': 'Select the spa manager this document belongs to.'
        }),
        ('Metadata (Auto-populated)', {
            'fields': ('manager_name', 'uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['manager_name', 'uploaded_by', 'created_at', 'updated_at', 'file_preview_detail']
    
    actions = ['download_selected_documents']
    
    def manager_display(self, obj):
        """Display manager name with link"""
        if obj.spa_manager:
            return format_html(
                '<a href="/admin/spas/spamanager/{}/change/">{}</a>',
                obj.spa_manager.id,
                obj.manager_name or obj.spa_manager.fullname
            )
        return "-"
    manager_display.short_description = 'Manager'
    
    def spa_display(self, obj):
        """Display spa information with link"""
        if obj.spa_manager and obj.spa_manager.spa:
            return format_html(
                '<a href="/admin/spas/spa/{}/change/">{} - {}</a>',
                obj.spa_manager.spa.id,
                obj.spa_manager.spa.spa_code,
                obj.spa_manager.spa.spa_name
            )
        return format_html('<span style="color: #999;">No Spa</span>')
    spa_display.short_description = 'Spa'
    
    def file_preview(self, obj):
        """Display file type icon and name"""
        if obj.file:
            file_ext = obj.file.name.split('.')[-1].upper()
            icon_map = {
                'PDF': '📄',
                'DOC': '📝',
                'DOCX': '📝',
                'XLS': '📊',
                'XLSX': '📊',
                'JPG': '🖼️',
                'JPEG': '🖼️',
                'PNG': '🖼️',
                'GIF': '🖼️',
                'ZIP': '📦',
                'RAR': '📦',
            }
            icon = icon_map.get(file_ext, '📎')
            filename = obj.file.name.split('/')[-1]
            return format_html(
                '{} <a href="{}" target="_blank">{}</a>',
                icon,
                obj.file.url,
                filename[:30] + '...' if len(filename) > 30 else filename
            )
        return '-'
    file_preview.short_description = 'File'
    
    def file_preview_detail(self, obj):
        """Display detailed file preview in form"""
        if obj.file:
            file_ext = obj.file.name.split('.')[-1].upper()
            file_size = self.file_size_display(obj)
            return format_html(
                '<div style="margin: 10px 0;">'
                '<p><strong>File:</strong> {}</p>'
                '<p><strong>Size:</strong> {}</p>'
                '<p><strong>Type:</strong> {}</p>'
                '<p><a href="{}" target="_blank" class="button">Download File</a></p>'
                '</div>',
                obj.file.name.split('/')[-1],
                file_size,
                file_ext,
                obj.file.url
            )
        return 'No file uploaded'
    file_preview_detail.short_description = 'File Preview'
    
    def file_size_display(self, obj):
        """Display file size in human-readable format"""
        if obj.file:
            try:
                size = obj.file.size
                if size < 1024:
                    return f"{size} B"
                elif size < 1024 * 1024:
                    return f"{size / 1024:.1f} KB"
                else:
                    return f"{size / (1024 * 1024):.1f} MB"
            except:
                return "Unknown"
        return "-"
    file_size_display.short_description = 'Size'
    
    def download_selected_documents(self, request, queryset):
        """Bulk action to download documents"""
        count = queryset.count()
        self.message_user(request, f"{count} documents selected. Individual download links are available in the list view.")
    download_selected_documents.short_description = "Download selected documents"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('spa_manager', 'spa_manager__spa', 'uploaded_by')

# Register your models here.
