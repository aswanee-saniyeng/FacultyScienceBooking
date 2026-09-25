from django.shortcuts import render, redirect, get_object_or_404
from .models import Room
from .forms import RoomForm


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/room_list.html', {'rooms': rooms})


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return redirect('create_booking_with_room', room_id=room.id)


def manage_rooms(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'admin':
        return redirect('home')

    rooms = Room.objects.all()

    return render(
        request,
        'rooms/manage_rooms.html',
        {'rooms': rooms}
    )

def add_room(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'admin':
        return redirect('home')

    if request.method == 'POST':
        form = RoomForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('manage_rooms')

    else:
        form = RoomForm()

    return render(
        request,
        'rooms/add_room.html',
        {'form': form}
    )


def edit_room(request, room_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'admin':
        return redirect('home')

    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            return redirect('manage_rooms')

    else:
        form = RoomForm(instance=room)

    return render(
        request,
        'rooms/edit_room.html',
        {
            'form': form,
            'room': room
        }
    )

def delete_room(request, room_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'admin':
        return redirect('home')

    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        room.delete()
        return redirect('manage_rooms')

    return render(
        request,
        'rooms/delete_room.html',
        {
            'room': room
        }
    )