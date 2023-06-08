from django import forms


class IncreaseBalanceForm(forms.Form):
    amount = forms.FloatField(min_value=0.0, step_size=1,
                              widget=forms.NumberInput(attrs={'placeholder': 'Enter amount'}))
