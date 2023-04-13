from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserLoginForm(forms.Form):
    username = forms.CharField(
        validators=[
            validators.MaxLengthValidator(150)
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(150)
        ]
    )
