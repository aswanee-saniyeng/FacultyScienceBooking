from django.shortcuts import render, redirect, get_object_or_404

from .models import Device
from .forms import DeviceForm


def device_list(request):

    devices = Device.objects.all()

    return render(request, 'devices/device_list.html', {'devices': devices})


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

        form = DeviceForm(request.POST)

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