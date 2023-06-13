from django import forms
from django.core import validators


class FriendRequestCreationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter email'
        }),
        validators=[
            validators.MaxLengthValidator(150)
        ]
    )
