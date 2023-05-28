from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput

from website.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = TextInput(attrs={
            'placeholder': 'Enter your username'
        })
        self.fields['email'].widget = TextInput(attrs={
            'placeholder': 'Enter your email'
        })
        self.fields['password1'].widget = TextInput(attrs={
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget = TextInput(attrs={
            'placeholder': 'Enter your password again'
        })
