from django.db import models
from django.conf import settings


class AccountHolder(models.Model):
    """Account holder information for machines"""
    full_name = models.CharField(max_length=150, help_text="Full name of account holder")
    designation = models.CharField(max_length=100, blank=True, null=True, help_text="Designation/Title")
    
    # Audit
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'account_holders'
        ordering = ['full_name']
        verbose_name = 'Account Holder'
        verbose_name_plural = 'Account Holders'
    
    def __str__(self):
        if self.designation:
            return f"{self.full_name} ({self.designation})"
        return self.full_name


class Machine(models.Model):
    """Machine installation record for spas (Excel-like centralized record)"""

    STATUS_CHOICES = [
        ('in_use', 'In Use'),
        ('not_in_use', 'Not In Use'),
        ('broken', 'Broken'),
    ]

    # --- Spa Info (Location is derived from Spa) ---
    spa = models.ForeignKey('spas.Spa', on_delete=models.SET_NULL, null=True, blank=True, related_name='machines', help_text="Spa where machine is installed (location inherited from spa)")

    # --- Machine Information ---
    serial_number = models.CharField(max_length=100, unique=True, help_text="Unique serial number")
    machine_code = models.CharField(max_length=100, blank=True, null=True, help_text="Unique internal code or ID")
    machine_name = models.CharField(max_length=100, blank=True, null=True, help_text="Display name or identifier")
    model_name = models.CharField(max_length=100, blank=True, null=True, help_text="Model/Type of machine")
    firmware_version = models.CharField(max_length=50, blank=True, null=True, help_text="Software version")

    # --- Banking / Account Info ---
    account_name = models.CharField(max_length=200, blank=True, null=True, help_text="Account name for transactions")
    bank_name = models.CharField(max_length=150, blank=True, null=True, help_text="Bank name")
    account_number = models.CharField(max_length=100, blank=True, null=True, help_text="Bank account number")
    acc_holder = models.ForeignKey(AccountHolder, on_delete=models.SET_NULL, blank=True, null=True, related_name='machines', help_text="Account holder")
    mid = models.CharField(max_length=100, blank=True, null=True, help_text="Merchant ID")
    tid = models.CharField(max_length=100, blank=True, null=True, help_text="Terminal ID")

    # --- Status & Meta ---
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_use')
    remark = models.TextField(blank=True, null=True, help_text="Additional notes or comments")

    # --- Audit Info ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='machines_created'
    )

    class Meta:
        db_table = 'machines'
        ordering = ['spa__spa_name', 'serial_number']
        indexes = [
            models.Index(fields=['serial_number'], name='idx_machine_serial'),
            models.Index(fields=['machine_code'], name='idx_machine_code'),
            models.Index(fields=['status'], name='idx_machine_status'),
            models.Index(fields=['spa'], name='idx_machine_spa'),
        ]
        verbose_name = 'Machine'
        verbose_name_plural = 'Machines'

    def __str__(self):
        return f"{self.machine_name or 'Machine'} ({self.serial_number}) - {self.spa.spa_name if self.spa else 'No Spa'}"
    
    @property
    def area(self):
        """Get area from spa's location"""
        return self.spa.area if self.spa else None
    
    @property
    def city(self):
        """Get city from spa's location"""
        if self.spa and self.spa.area:
            return self.spa.area.city
        return None
    
    @property
    def state(self):
        """Get state from spa's location"""
        if self.spa and self.spa.area and self.spa.area.city:
            return self.spa.area.city.state
        return None
