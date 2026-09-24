from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'room',
        'device',
        'booking_date',
        'start_time',
        'end_time',
        'status',
    )

    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'purpose')