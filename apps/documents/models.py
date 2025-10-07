from django.db import models
from django.conf import settings


class DocumentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'document_types'
        ordering = ['name']

    def __str__(self):
        return self.name


def document_upload_path(instance, filename):
    return f"documents/user_{instance.user_id}/{filename}"


class Document(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='documents', on_delete=models.PROTECT, null=True, blank=True)
    doc_type = models.ForeignKey(DocumentType, related_name='documents', on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=document_upload_path)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='documents_uploaded', on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'documents'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'doc_type'], name='idx_doc_user_type'),
        ]

    def __str__(self):
        return f"{self.title} ({self.doc_type.name})"

# Create your models here.
