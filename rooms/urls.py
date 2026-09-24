from django.urls import path

from .views import room_list, book_room

urlpatterns = [
    path('', room_list, name='room_list'),
    path('book/<int:room_id>/', book_room, name='book_room'),
]