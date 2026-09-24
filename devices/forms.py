from django import forms
from .models import Device


class DeviceForm(forms.ModelForm):

    class Meta:
        model = Device

        fields = [
            'device_name',
            'device_type',
            'quantity',
            'description',
            'status',
        ]

        widgets = {

            'device_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter device name'
                }
            ),

            'device_type': forms.TextInput(
                attrs={
                    'placeholder': 'Enter device type'
                }
            ),

            'quantity': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter quantity',
                    'min': '1'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter device description'
                }
            ),

            'status': forms.Select(),
        }