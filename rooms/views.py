from django.shortcuts import render, redirect, get_object_or_404
from .models import Room


def room_list(request):
    rooms = Room.objects.all()

    return render(
        request,
        'rooms/room_list.html',
        {'rooms': rooms}
    )


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    return redirect('create_booking_with_room', room_id=room.id)