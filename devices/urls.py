from django.urls import path

from .views import (
    device_list,
    book_device,
    manage_devices,
    add_device,
    edit_device,
    delete_device,
)


urlpatterns = [

    path('', device_list, name='device_list'),

    path('book/<int:device_id>/', book_device, name='book_device'),

    path('manage/', manage_devices, name='manage_devices'),

    path('add/', add_device, name='add_device'),

    path(
        'edit/<int:device_id>/',
        edit_device,
        name='edit_device'
    ),

    path(
        'delete/<int:device_id>/',
        delete_device,
        name='delete_device'
    ),

]