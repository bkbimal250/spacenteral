from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class SimCard(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_SUSPENDED = 'suspended'
    STATUS_CLOSED = 'closed'
    STATUS_LOST = 'lost'

    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_SUSPENDED, 'Suspended'),
        (STATUS_CLOSED, 'Closed'),
        (STATUS_LOST, 'Lost'),
    ]

    mobile_validator = RegexValidator(
        regex=r'^[6-9]\d{9}$',
        message="Enter a valid 10-digit Indian mobile number"
    )

    date_of_issue = models.DateField()
    mobile_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[mobile_validator]
    )
    simcard_serial_number = models.CharField(max_length=50, unique=True)
    sim_owner_name = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE
    )

    spa = models.ForeignKey(
        'spas.Spa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='simcards'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='simcards_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='simcards_updated'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.mobile_number} ({self.get_status_display()})"
