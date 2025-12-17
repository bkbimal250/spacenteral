# apps/spas/models.py
from django.db import models
from django.conf import settings


class PrimaryOwner(models.Model):
    """Independent Primary Owner model"""
    fullname = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'primary_owners'
        ordering = ['fullname']

    def __str__(self):
        return self.fullname


class SecondaryOwner(models.Model):
    """Independent Secondary Owner model"""
    fullname = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'secondary_owners'
        ordering = ['fullname']

    def __str__(self):
        return self.fullname


class ThirdOwner(models.Model):
    """Independent Third Owner model"""
    fullname = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'third_owners'
        ordering = ['fullname']

    def __str__(self):
        return self.fullname


class FourthOwner(models.Model):
    """Independent Fourth Owner model"""
    fullname = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'fourth_owners'
        ordering = ['fullname']

    def __str__(self):
        return self.fullname


class Spa(models.Model):
    spa_code = models.CharField(max_length=50, unique=True)
    spa_name = models.CharField(max_length=200)
    area = models.ForeignKey('location.Area', on_delete=models.SET_NULL, null=True, related_name='spas')

    # One-to-many relationships with independent owner models
    # One Primary Owner can manage multiple spas, but each spa has only ONE primary owner
    primary_owner = models.ForeignKey(
        'PrimaryOwner',
        on_delete=models.SET_NULL,
        null=True,
        related_name='spas',
        help_text="Primary Owner (required for spa creation)"
    )
    
    # One Secondary Owner can manage multiple spas, but each spa has only ONE secondary owner (optional)
    secondary_owner = models.ForeignKey(
        'SecondaryOwner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='spas',
        help_text="Secondary Owner (optional)"
    )
    
    # One Third Owner can manage multiple spas, but each spa has only ONE third owner (optional)
    third_owner = models.ForeignKey(
        'ThirdOwner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='spas',
        help_text="Third Owner (optional)"
    )
    
    # One Fourth Owner can manage multiple spas, but each spa has only ONE fourth owner (optional)
    fourth_owner = models.ForeignKey(
        'FourthOwner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='spas',
        help_text="Fourth Owner (optional)"
    )
    
    spamanager = models.CharField(max_length=200, blank=True, null=True)
    opening_date = models.DateField(null=True, blank=True)

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Temporarily Closed', 'Temporarily Closed'),
        ('Processing', 'Processing'),
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Open')

    line_track = models.CharField(max_length=100, blank=True, null=True)
    landmark = models.CharField(max_length=200, blank=True, null=True)

    # multiple contact options (comma-separated list)
    emails = models.TextField(blank=True, null=True, help_text="Comma-separated list of emails")
    phones = models.TextField(blank=True, null=True, help_text="Comma-separated list of phone numbers")

    address = models.TextField(blank=True, null=True)
    google_map_link = models.TextField(blank=True, null=True, help_text="Google Maps link for spa location (supports long embed URLs)")
    google_drive_link = models.URLField(blank=True, null=True, help_text="Google Drive link for spa photos and videos")

    AGREEMENT_STATUS_CHOICES = [
        ('done', 'Done'),
        ('pending', 'Pending'),
       
    ]

    agreement_status = models.CharField(max_length=50, choices=AGREEMENT_STATUS_CHOICES, default='pending')
    remark = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='spas_created'
    )

    class Meta:
        db_table = 'spas'
        indexes = [
            models.Index(fields=['spa_code'], name='idx_spa_code'),
            models.Index(fields=['status'], name='idx_spa_status'),
            models.Index(fields=['spa_name'], name='idx_spa_name'),
        ]
        ordering = ['spa_name']

    def __str__(self):
        return f"{self.spa_name} ({self.spa_code})"

    # Utility functions (optional)
    def get_email_list(self):
        """Return list of emails (split by comma)"""
        return [e.strip() for e in self.emails.split(',')] if self.emails else []

    def get_phone_list(self):
        """Return list of phones (split by comma)"""
        return [p.strip() for p in self.phones.split(',')] if self.phones else []

    # Location helpers
    @property
    def city(self):
        return self.area.city if self.area else None

    @property
    def state(self):
        return self.area.city.state if self.area and self.area.city else None



class SpaManager(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    spa = models.ForeignKey(Spa, on_delete=models.SET_NULL, null=True, related_name='managers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'spa_managers'
        ordering = ['fullname']

    def __str__(self):
        return self.fullname
    
    @property
    def spa_name(self):
        return self.spa.spa_name if self.spa and self.spa.spa_name else None
    
 
class SocialMediaLink(models.Model):
    spa = models.ForeignKey(Spa, on_delete=models.CASCADE, related_name='social_media_links')
    platform = models.CharField(max_length=100,null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'spa_social_media_links'
        ordering = ['platform']

    def __str__(self):
        return f"{self.platform} - {self.spa.spa_name}"
    
category_choices = [
    ('Business site', 'business site'),
    ('Advert site', 'advert site'),
    ('Booking site', 'booking site'),

]

class SpaWebsite(models.Model):
    spa = models.ForeignKey(Spa, on_delete=models.CASCADE, related_name='websites')
    category = models.CharField(max_length=100, choices=category_choices)
    url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by= models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='spa_websites_created'
    )

    class Meta:
        db_table = 'spa_websites'
        ordering = ['url']

    def __str__(self):
        return f"Website for {self.spa.spa_name}: {self.url}"


# Media file model using google drive link only(we add google drive link of photo videos)
class SpaMedia(models.Model):
    spa = models.ForeignKey(Spa, on_delete=models.CASCADE, related_name='media')
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='spa_media_created'
    )

    class Meta:
        db_table = 'spa_media'
        ordering = ['url']

    def __str__(self):
        return f"Media for {self.spa.spa_name}: {self.url}"