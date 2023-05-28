from django import forms
from django.core import validators


class FriendRequestCreationForm(forms.Form):
    email = forms.EmailField(
        validators=[
            validators.MaxLengthValidator(150)
        ]
    )
