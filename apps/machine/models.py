from django.db import models
from django.conf import settings


class Machine(models.Model):
    """Card swipe machine installed at spas"""
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
        ('retired', 'Retired'),
    )

    # Unique identifiers
    serial_number = models.CharField(max_length=100, unique=True)
    model_name = models.CharField(max_length=100)
    firmware_version = models.CharField(max_length=50, blank=True, null=True)

    # Assignment
    spa = models.ForeignKey('spas.Spa', related_name='machines', on_delete=models.PROTECT)
    installed_area = models.ForeignKey('location.Area', related_name='machines', on_delete=models.PROTECT)

    # Network/placement
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    location_note = models.CharField(max_length=200, blank=True, null=True, help_text='e.g., Front desk, Room 1')

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    activated_at = models.DateField(blank=True, null=True)
    last_service_date = models.DateField(blank=True, null=True)

    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='machines_created', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'machines'
        ordering = ['serial_number']
        indexes = [
            models.Index(fields=['serial_number'], name='idx_machine_sn'),
            models.Index(fields=['spa', 'status'], name='idx_machine_spa_status'),
        ]

    def __str__(self):
        return f"{self.serial_number} - {self.model_name}"


class MachineAssignment(models.Model):
    """History of machine reassignments between spas/areas"""
    machine = models.ForeignKey(Machine, related_name='assignments', on_delete=models.CASCADE)
    from_spa = models.ForeignKey('spas.Spa', related_name='machine_moves_from', on_delete=models.SET_NULL, null=True, blank=True)
    to_spa = models.ForeignKey('spas.Spa', related_name='machine_moves_to', on_delete=models.PROTECT)
    from_area = models.ForeignKey('location.Area', related_name='machine_moves_from', on_delete=models.SET_NULL, null=True, blank=True)
    to_area = models.ForeignKey('location.Area', related_name='machine_moves_to', on_delete=models.PROTECT)
    moved_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'machine_assignments'
        ordering = ['-moved_at']

    def __str__(self):
        return f"{self.machine.serial_number}: {self.from_spa} -> {self.to_spa}"

# Create your models here.
