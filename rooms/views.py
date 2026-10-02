from datetime import date
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from bookings.models import Booking
from .models import Room
from .forms import RoomForm


TIME_SLOTS = [
    ('08:00-10:00', '08:00 - 10:00'),
    ('10:00-12:00', '10:00 - 12:00'),
    ('13:00-15:00', '13:00 - 15:00'),
    ('15:00-17:00', '15:00 - 17:00'),
]


def room_list(request):

    selected_date = request.GET.get('date') or date.today().isoformat()
    selected_slot = request.GET.get('slot') or TIME_SLOTS[0][0]
    start_time, end_time = selected_slot.split('-')

    all_rooms = Room.objects.all().order_by('room_name')

    busy_room_ids = set(
        Booking.objects.filter(
            room__isnull=False,
            booking_date=selected_date,
            status__in=['pending', 'approved'],
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).values_list('room_id', flat=True)
    )

    for room in all_rooms:
        room.is_available_now = (
            room.status == 'available'
            and room.id not in busy_room_ids
        )

    paginator = Paginator(all_rooms, 9)
    rooms = paginator.get_page(request.GET.get('page'))

    context = {
        'rooms': rooms,
        'time_slots': TIME_SLOTS,
        'selected_date': selected_date,
        'selected_slot': selected_slot,
    }
    return render(request, 'rooms/room_list.html', context)


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
        form = RoomForm(request.POST, request.FILES)

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
        form = RoomForm(request.POST, request.FILES, instance=room)

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