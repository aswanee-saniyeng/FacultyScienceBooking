from django import forms
from .models import Room


class RoomForm(forms.ModelForm):

    class Meta:
        model = Room

        fields = [
            'room_name',
            'building',
            'capacity',
            'description',
            'status',
        ]

        widgets = {
            'room_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter room name'
                }
            ),

            'building': forms.TextInput(
                attrs={
                    'placeholder': 'Enter building'
                }
            ),

            'capacity': forms.NumberInput(
                attrs={
                    'placeholder': 'Enter capacity',
                    'min': '1'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Enter room description'
                }
            ),

            'status': forms.Select(),
        }