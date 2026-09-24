from django.shortcuts import render, redirect, get_object_or_404
from .models import Device


def device_list(request):
    devices = Device.objects.all()
    return render(request, 'devices/device_list.html', {'devices': devices})


def book_device(request, device_id):
    device = get_object_or_404(Device, id=device_id)
    return redirect('create_booking_with_device', device_id=device.id)