from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'password1',
            'password2',
        ]

class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'role',
            'is_active',
        ]

        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'First name'}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Last name'}
            ),
            'email': forms.EmailInput(
                attrs={'placeholder': 'Email'}
            ),
            'role': forms.Select(),
        }