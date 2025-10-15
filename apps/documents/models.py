from django.db import models
from django.conf import settings


def spa_manager_document_upload_path(instance, filename):
    """Store spa manager docs based on spa manager ID."""
    if instance.spa_manager_id:
        return f"documents/spa_manager_{instance.spa_manager_id}/{filename}"
    return f"documents/spa_manager_unassigned/{filename}"


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


def owner_document_upload_path(instance, filename):
    """Store owner docs based on owner type and ID."""
    if instance.primary_owner_id:
        return f"documents/primary_owner_{instance.primary_owner_id}/{filename}"
    elif instance.secondary_owner_id:
        return f"documents/secondary_owner_{instance.secondary_owner_id}/{filename}"
    elif instance.third_owner_id:
        return f"documents/third_owner_{instance.third_owner_id}/{filename}"
    elif instance.fourth_owner_id:
        return f"documents/fourth_owner_{instance.fourth_owner_id}/{filename}"
    return f"documents/owner_unassigned/{filename}"


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


class OwnerDocument(models.Model):
    """Documents for Spa Owners - Primary, Secondary, Third, and Fourth owners"""
    
    # Owner relationships - only one should be set at a time
    primary_owner = models.ForeignKey(
        'spas.PrimaryOwner',
        related_name='documents',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Primary owner this document belongs to"
    )
    secondary_owner = models.ForeignKey(
        'spas.SecondaryOwner',
        related_name='documents',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Secondary owner this document belongs to"
    )
    third_owner = models.ForeignKey(
        'spas.ThirdOwner',
        related_name='documents',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Third owner this document belongs to"
    )
    fourth_owner = models.ForeignKey(
        'spas.FourthOwner',
        related_name='documents',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Fourth owner this document belongs to"
    )
    
    # Document fields
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=owner_document_upload_path)
    notes = models.TextField(blank=True, null=True)
    
    # Metadata
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='owner_documents_uploaded',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Denormalized owner info for quick access
    owner_name = models.CharField(max_length=200, blank=True, null=True)
    owner_type = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        help_text="Type of owner: primary, secondary, third, or fourth"
    )

    class Meta:
        db_table = 'owner_documents'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['primary_owner'], name='idx_odoc_primary'),
            models.Index(fields=['secondary_owner'], name='idx_odoc_secondary'),
            models.Index(fields=['third_owner'], name='idx_odoc_third'),
            models.Index(fields=['fourth_owner'], name='idx_odoc_fourth'),
            models.Index(fields=['owner_type'], name='idx_odoc_type'),
            models.Index(fields=['title'], name='idx_odoc_title'),
        ]

    def __str__(self):
        owner = self.get_owner_name()
        return f"{self.title} - {owner}"
    
    def get_owner_name(self):
        """Get the name of the associated owner"""
        if self.primary_owner:
            return self.primary_owner.fullname
        elif self.secondary_owner:
            return self.secondary_owner.fullname
        elif self.third_owner:
            return self.third_owner.fullname
        elif self.fourth_owner:
            return self.fourth_owner.fullname
        return "Unknown Owner"
    
    def get_owner_type(self):
        """Get the type of owner"""
        if self.primary_owner:
            return "primary"
        elif self.secondary_owner:
            return "secondary"
        elif self.third_owner:
            return "third"
        elif self.fourth_owner:
            return "fourth"
        return None
    
    def save(self, *args, **kwargs):
        # Populate denormalized fields
        self.owner_name = self.get_owner_name()
        self.owner_type = self.get_owner_type()
        
        # Validation: Ensure only one owner is set
        owners_set = sum([
            bool(self.primary_owner),
            bool(self.secondary_owner),
            bool(self.third_owner),
            bool(self.fourth_owner)
        ])
        
        if owners_set == 0:
            raise ValueError("At least one owner must be specified for the document")
        if owners_set > 1:
            raise ValueError("Only one owner can be specified per document")
        
        super().save(*args, **kwargs)



class SpaManagerDocument(models.Model):
    """Documents for Spa Managers"""
    spa_manager = models.ForeignKey(
        'spas.SpaManager', 
        on_delete=models.CASCADE, 
        related_name='documents',
        help_text="Spa manager this document belongs to"
    )
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=spa_manager_document_upload_path)
    notes = models.TextField(blank=True, null=True)
    
    # Metadata
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='spa_manager_documents_uploaded',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Denormalized info for quick access
    manager_name = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        db_table = 'spa_manager_documents'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['spa_manager'], name='idx_smdoc_spa_manager'),
            models.Index(fields=['title'], name='idx_smdoc_title'),
        ]

    def __str__(self):
        manager_name = self.spa_manager.fullname if self.spa_manager else "Unknown Manager"
        return f"{self.title} - {manager_name}"
    
    def save(self, *args, **kwargs):
        # Populate denormalized fields
        if self.spa_manager:
            self.manager_name = self.spa_manager.fullname
        super().save(*args, **kwargs)


