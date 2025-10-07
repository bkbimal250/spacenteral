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
    list_display = ['title', 'doc_type', 'user', 'uploaded_by', 'created_at']
    list_filter = ['doc_type', 'user']
    search_fields = ['title', 'user__email']
    raw_id_fields = ['user', 'uploaded_by']
    ordering = ['-created_at']

# Register your models here.
