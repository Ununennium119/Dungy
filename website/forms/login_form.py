from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.core import validators


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username'}
        ),
        validators=[
            validators.MaxLengthValidator(150)
        ]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password'}
        ),
        validators=[
            validators.MaxLengthValidator(150)
        ]
    )
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label="")


