from django import forms

from website.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
