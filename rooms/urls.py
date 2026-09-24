from django.urls import path
from .views import room_list, book_room, manage_rooms, add_room, edit_room, delete_room

urlpatterns = [
    path('', room_list, name='room_list'),
    path('book/<int:room_id>/', book_room, name='book_room'),
    path('manage/', manage_rooms, name='manage_rooms'),
    path('add/', add_room, name='add_room'),
    path('edit/<int:room_id>/', edit_room, name='edit_room'),
    path('delete/<int:room_id>/', delete_room, name='delete_room'),
]