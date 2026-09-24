from django.db import models


class Device(models.Model):

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]

    device_name = models.CharField(max_length=100)

    device_type = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField(default=1)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    def __str__(self):
        return self.device_name