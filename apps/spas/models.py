# apps/spas/models.py
from django.db import models
from django.conf import settings

class SpaOwner(models.Model):
    fullname = models.CharField(max_length=200)
    parent_owner = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'spa_owners'
        ordering = ['fullname']

    def __str__(self):
        if self.parent_owner:
            return f"{self.fullname} (Sub-owner of {self.parent_owner.fullname})"
        return self.fullname



class Spa(models.Model):
    spa_code = models.CharField(max_length=50, unique=True)
    spa_name = models.CharField(max_length=200)
    area = models.ForeignKey('location.Area', on_delete=models.SET_NULL, null=True, related_name='spas')

    # Linked to one primary owner
    owner = models.ForeignKey('SpaOwner', on_delete=models.SET_NULL, null=True, related_name='spas')
    # Additional sub-owners/managers (optional)
    sub_owners = models.ManyToManyField('SpaOwner', blank=True, related_name='managed_spas')

    opening_date = models.DateField(null=True, blank=True)
    reopen_date = models.DateField(null=True, blank=True)

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Temporarily Closed', 'Temporarily Closed')
    ]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Open')

    line_track = models.CharField(max_length=100, blank=True, null=True)
    landmark = models.CharField(max_length=200, blank=True, null=True)

    # multiple contact options (comma-separated list)
    emails = models.TextField(blank=True, null=True, help_text="Comma-separated list of emails")
    phones = models.TextField(blank=True, null=True, help_text="Comma-separated list of phone numbers")

    address = models.TextField(blank=True, null=True)

    AGREEMENT = [
        ('Active', 'Active'),
        ('Expired', 'Expired'),
        ('Not Avail', 'Not Avail')
    ]
    agreement_status = models.CharField(max_length=50, choices=AGREEMENT, default='Not Avail')
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
