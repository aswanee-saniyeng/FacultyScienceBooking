from django.urls import path

from .views import device_list, book_device


urlpatterns = [

    path('', device_list, name='device_list'),

    path('book/<int:device_id>/', book_device, name='book_device'),

]