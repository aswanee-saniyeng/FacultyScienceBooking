from django.contrib import admin
from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'device_type', 'quantity', 'status', 'image')
    search_fields = ('device_name', 'device_type')