from django.urls import path
from .views import create_booking, my_bookings, cancel_booking, booking_report, manage_bookings, update_booking_status
urlpatterns = [

    path(
        'create/',
        create_booking,
        name='create_booking'
    ),

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

    path(
        'my/',
        my_bookings,
        name='my_bookings'
    ),

    path(
        'cancel/<int:booking_id>/',
        cancel_booking,
        name='cancel_booking'
    ),

    path(
        'report/',
        booking_report,
        name='booking_report'
    ),

    path(
        'manage/',
        manage_bookings,
        name='manage_bookings'
    ),

    path(
    'manage/<int:booking_id>/approve/',
    update_booking_status,
    {'status': 'approved'},
    name='approve_booking'
),

path(
    'manage/<int:booking_id>/reject/',
    update_booking_status,
    {'status': 'rejected'},
    name='reject_booking'
),

]