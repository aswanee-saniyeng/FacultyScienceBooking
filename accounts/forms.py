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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['role'].choices = [
            choice for choice in User.ROLE_CHOICES
            if choice[0] != 'admin'
        ]

        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        if not email.lower().endswith('@ftu.ac.th'):
            raise forms.ValidationError(
                'Please register using your Fatoni University email address (must end with @ftu.ac.th).'
            )

        return email