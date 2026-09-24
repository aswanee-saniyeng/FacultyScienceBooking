from django.conf import settings
from django.db import models

from rooms.models import Room
from devices.models import Device


class Booking(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True,
        blank=True
    )

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True,
        blank=True
    )

    booking_date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    purpose = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.booking_date}"