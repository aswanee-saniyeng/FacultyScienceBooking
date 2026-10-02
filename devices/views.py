from datetime import date
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from bookings.models import Booking
from .models import Device
from .forms import DeviceForm


TIME_SLOTS = [
    ('08:00-10:00', '08:00 - 10:00'),
    ('10:00-12:00', '10:00 - 12:00'),
    ('13:00-15:00', '13:00 - 15:00'),
    ('15:00-17:00', '15:00 - 17:00'),
]


def device_list(request):

    selected_date = request.GET.get('date') or date.today().isoformat()
    selected_slot = request.GET.get('slot') or TIME_SLOTS[0][0]
    start_time, end_time = selected_slot.split('-')

    all_devices = Device.objects.all().order_by('device_name')

    busy_device_ids = set(
        Booking.objects.filter(
            device__isnull=False,
            booking_date=selected_date,
            status__in=['pending', 'approved'],
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).values_list('device_id', flat=True)
    )

    for device in all_devices:
        device.is_available_now = (
            device.status == 'available'
            and device.id not in busy_device_ids
        )

    paginator = Paginator(all_devices, 8)
    devices = paginator.get_page(request.GET.get('page'))

    context = {
        'devices': devices,
        'time_slots': TIME_SLOTS,
        'selected_date': selected_date,
        'selected_slot': selected_slot,
    }
    return render(request, 'devices/device_list.html', context)


def book_device(request, device_id):

    device = get_object_or_404(Device, id=device_id)

    return redirect('create_booking_with_device', device_id=device.id)


def manage_devices(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'admin':
        return redirect('home')

    devices = Device.objects.all()

    return render(
        request,
        'devices/manage_devices.html',
        {
            'devices': devices,
        }
    )

def add_device(request):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'admin':
        return redirect('home')

    if request.method == 'POST':

        form = DeviceForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('manage_devices')

    else:

        form = DeviceForm()

    return render(
        request,
        'devices/add_device.html',
        {
            'form': form,
        }
    )

def edit_device(request, device_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'admin':
        return redirect('home')

    device = get_object_or_404(Device, id=device_id)

    if request.method == 'POST':

        form = DeviceForm(
            request.POST,
            request.FILES,
            instance=device
        )

        if form.is_valid():
            form.save()
            return redirect('manage_devices')

    else:

        form = DeviceForm(instance=device)

    return render(
        request,
        'devices/edit_device.html',
        {
            'form': form,
            'device': device,
        }
    )

def delete_device(request, device_id):

    if not request.user.is_authenticated:
        return redirect('login')

    if request.user.role != 'admin':
        return redirect('home')

    device = get_object_or_404(Device, id=device_id)

    if request.method == 'POST':
        device.delete()
        return redirect('manage_devices')

    return render(
        request,
        'devices/delete_device.html',
        {
            'device': device,
        }
    )