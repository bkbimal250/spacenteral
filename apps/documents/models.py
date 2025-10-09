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
    """Store docs under spa when available, else under 'unassigned'."""
    if getattr(instance, 'spa_id', None):
        return f"documents/spa_{instance.spa_id}/{filename}"
    return f"documents/unassigned/{filename}"


class Document(models.Model):
    # Optional legacy user fields (kept for backward compatibility)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='documents',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        help_text="Primary user (legacy field)"
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='shared_documents',
        blank=True,
        help_text="Users who have access to this document (legacy, optional)"
    )

    # New: Link documents to Spa (public, not user-specific)
    spa = models.ForeignKey(
        'spas.Spa',
        related_name='documents',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Spa this document belongs to"
    )
    
    doc_type = models.ForeignKey(DocumentType, related_name='documents', on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=document_upload_path)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='documents_uploaded', 
        on_delete=models.SET_NULL, 
        null=True
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Denormalized Spa info for search/sorting and stability
    spa_code = models.CharField(max_length=50, blank=True, null=True)
    spa_name = models.CharField(max_length=200, blank=True, null=True)
    state_name = models.CharField(max_length=100, blank=True, null=True)
    city_name = models.CharField(max_length=100, blank=True, null=True)
    area_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'documents'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['doc_type'], name='idx_doc_type'),
            models.Index(fields=['spa'], name='idx_doc_spa'),
            models.Index(fields=['spa_code'], name='idx_doc_spa_code'),
            models.Index(fields=['title'], name='idx_doc_title'),
        ]

    def __str__(self):
        return f"{self.title} ({self.doc_type.name})"
    
    def save(self, *args, **kwargs):
        # Populate denormalized spa fields
        if self.spa:
            self.spa_code = getattr(self.spa, 'spa_code', None)
            self.spa_name = getattr(self.spa, 'spa_name', None)
            # Walk area → city → state names if present
            try:
                self.area_name = getattr(self.spa.area, 'name', None) if getattr(self.spa, 'area', None) else None
                self.city_name = getattr(self.spa.area.city, 'name', None) if getattr(self.spa, 'area', None) and getattr(self.spa.area, 'city', None) else None
                self.state_name = getattr(self.spa.area.city.state, 'name', None) if getattr(self.spa, 'area', None) and getattr(self.spa.area, 'city', None) and getattr(self.spa.area.city, 'state', None) else None
            except Exception:
                # Do not block save due to optional relations
                pass

        super().save(*args, **kwargs)
        # Legacy auto-sync: if users is empty but user is set, add user to users
        if self.user and not self.users.exists():
            self.users.add(self.user)

# Create your models here.
