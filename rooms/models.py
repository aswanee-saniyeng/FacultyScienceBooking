from django.db import models


class Room(models.Model):

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]

    room_name = models.CharField(max_length=100)

    building = models.CharField(max_length=100)

    capacity = models.PositiveIntegerField()

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )

    def __str__(self):
        return self.room_name