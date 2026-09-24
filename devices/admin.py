from django.contrib import admin
from .models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'device_type', 'quantity', 'status')
    list_filter = ('status', 'device_type')
    search_fields = ('device_name', 'device_type')