from django import forms

from website.models import Cost, Group


class CostUpdateForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['description', 'image', 'note', 'archived']
