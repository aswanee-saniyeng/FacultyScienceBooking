from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'building', 'capacity', 'status')
    list_filter = ('status', 'building')
    search_fields = ('room_name', 'building')