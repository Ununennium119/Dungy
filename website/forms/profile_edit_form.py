from django import forms
from django.core import validators


class ProfileForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username'
        }
        ),
        validators=[
            validators.MaxLengthValidator(150)
        ]
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your email'}
        ),
        validators=[
            validators.MaxLengthValidator(150)
        ]
    )
