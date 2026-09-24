from django.urls import path
from .views import create_booking, my_bookings, cancel_booking, booking_report


urlpatterns = [
    path('create/', create_booking, name='create_booking'),

    path(
        'create/room/<int:room_id>/',
        create_booking,
        name='create_booking_with_room'
    ),

    path(
        'create/device/<int:device_id>/',
        create_booking,
        name='create_booking_with_device'
    ),

    path('my/', my_bookings, name='my_bookings'),

    path(
        'cancel/<int:booking_id>/',
        cancel_booking,
        name='cancel_booking'
    ),

    path('report/', booking_report, name='booking_report'),
]