from django import forms

from website.models import Cost, Group


class CostCreationForm(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ['description', 'amount', 'paid_by', 'date', 'image', 'note']

    def __init__(self, *args, **kwargs):
        group: Group = kwargs.pop('group')

        super(CostCreationForm, self).__init__(*args, **kwargs)

        group_users = group.members.all()
        self.fields['members'] = forms.ModelMultipleChoiceField(
            queryset=group_users
        )
        self.fields['paid_by'].queryset = group_users

        self.fields['date'].widget = forms.widgets.DateInput(
            attrs={'type': 'date'}
        )
