from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            'room',
            'device',
            'booking_date',
            'start_time',
            'end_time',
            'purpose',
        ]

        widgets = {
            'booking_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'start_time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
            'end_time': forms.TimeInput(
                attrs={'type': 'time'}
            ),
            'purpose': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter the purpose of booking'
                }
            ),
        }