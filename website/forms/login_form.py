from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.core import validators


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
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, label="")
