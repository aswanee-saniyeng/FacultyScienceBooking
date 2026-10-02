
from django.contrib import admin
from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):

    list_display = (
        'device_name',
        'device_type',
        'status',
    )

    list_filter = (
        'device_type',
        'status',
    )

    search_fields = (
        'device_name',
        'device_type',
        'description',
    )

    fields = (
        'device_name',
        'device_type',
        'description',
        'status',
        'image',
    )
