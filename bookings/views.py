from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count

from .forms import BookingForm
from rooms.models import Room
from devices.models import Device
from .models import Booking


@login_required
def create_booking(request, room_id=None, device_id=None):

    room = None
    device = None

    if room_id:
        room = Room.objects.get(id=room_id)

    if device_id:
        device = Device.objects.get(id=device_id)

<<<<<<< HEAD
    # =========================
    # POST - Submit booking
    # =========================
    if request.method == 'POST':

        form = BookingForm(request.POST)
=======
        if request.method == 'POST':
            form = BookingForm(request.POST)
>>>>>>> d654ec89752c26836767092f0c323650862db46a

            if form.is_valid():

                booking_date = form.cleaned_data['booking_date']
                start_time = form.cleaned_data['start_time']
                end_time = form.cleaned_data['end_time']
                selected_room = form.cleaned_data['room']
                selected_device = form.cleaned_data['device']

                overlapping_bookings = Booking.objects.filter(
                    booking_date=booking_date,
                    start_time__lt=end_time,
                    end_time__gt=start_time
                ).exclude(
                    status__in=['cancelled', 'rejected']
                )

                if selected_room:
                    room_conflict = overlapping_bookings.filter(
                        room=selected_room
                    ).exists()

                    if room_conflict:
                        form.add_error(
                            'room',
                            'This room is already booked during the selected time.'
                        )

                if selected_device:
                    device_conflict = overlapping_bookings.filter(
                        device=selected_device
                    ).exists()

                    if device_conflict:
                        form.add_error(
                            'device',
                            'This device is already booked during the selected time.'
                        )

                if not form.errors:

                    booking = form.save(commit=False)
                    booking.user = request.user
                    booking.save()

                    return redirect('home')

    # =========================
    # GET - Open booking page
    # =========================
    else:

        initial_data = {}

        selected_date = request.GET.get('date')
        selected_slot = request.GET.get('slot')

        if selected_date:
            initial_data['booking_date'] = selected_date

        if selected_slot and '-' in selected_slot:
            start_time, end_time = selected_slot.split('-')
            initial_data['start_time'] = start_time
            initial_data['end_time'] = end_time

        if room:
            initial_data['room'] = room

        elif device:
            initial_data['device'] = device

        form = BookingForm(initial=initial_data)

        return render(
            request,
            'bookings/create_booking.html',
            {
                'form': form,
                'room': room,
                'device': device,
            }
        )


@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-booking_date', '-start_time')

    return render(
        request,
        'bookings/my_bookings.html',
        {
            'bookings': bookings,
        }
    )


@login_required
def cancel_booking(request, booking_id):

    booking = Booking.objects.get(
        id=booking_id,
        user=request.user
    )

    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()

    return redirect('my_bookings')

@login_required
def booking_report(request):

    # Only Admin can access the booking report
    if request.user.role != 'admin':
        return redirect('home')

    status = request.GET.get('status')
    booking_date = request.GET.get('booking_date')

    # All bookings for summary
    all_bookings = Booking.objects.all()

    summary = {
        'total': all_bookings.count(),
        'pending': all_bookings.filter(status='pending').count(),
        'approved': all_bookings.filter(status='approved').count(),
        'rejected': all_bookings.filter(status='rejected').count(),
        'cancelled': all_bookings.filter(status='cancelled').count(),
    }

    # Bookings for the report table
    bookings = all_bookings.order_by(
        '-booking_date',
        '-start_time'
    )

    if status:
        bookings = bookings.filter(status=status)

    if booking_date:
        bookings = bookings.filter(booking_date=booking_date)

    return render(
        request,
        'bookings/booking_report.html',
        {
            'bookings': bookings,
            'selected_status': status,
            'selected_date': booking_date,
            'summary': summary,
        }
    )

@login_required
def manage_bookings(request):

    # Only Admin can access this page
    if request.user.role != 'admin':
        return redirect('home')

    bookings = Booking.objects.all().select_related(
        'user',
        'room',
        'device'
    ).order_by(
        '-booking_date',
        '-start_time'
    )

    return render(
        request,
        'bookings/manage_bookings.html',
        {
            'bookings': bookings,
        }
    )

@login_required
def update_booking_status(request, booking_id, status):

    # Only Admin can update booking status
    if request.user.role != 'admin':
        return redirect('home')

    booking = Booking.objects.get(id=booking_id)

    if request.method == 'POST':

        if status in ['approved', 'rejected']:
            booking.status = status
            booking.save()

    return redirect('manage_bookings')