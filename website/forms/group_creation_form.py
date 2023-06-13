from django import forms

from website.models import Group


class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'type', 'image']
        labels = {'name': 'GROUP NAME', 'type': 'GROUP TYPE', 'image': ''}

    def __init__(self, *args, **kwargs):
        try:
            members_fields_count = int(kwargs.pop('members_fields_count', 3))
        except (ValueError, TypeError):
            members_fields_count = 3

        super(GroupCreationForm, self).__init__(*args, **kwargs)

        self.fields['members_fields_count'] = forms.CharField(widget=forms.HiddenInput(attrs={'autocomplete': 'off'}))

        self.fields['members_fields_count'].initial = members_fields_count
        for i in range(members_fields_count):
            self.fields[f'member_{i}'] = forms.EmailField(label='', required=False,
                                                          widget=forms.TextInput(
                                                              attrs={'autocomplete': 'off',
                                                                     'placeholder': 'Enter member\'s email'}))

        self.fields['name'].widget = forms.TextInput(attrs={
            'placeholder': 'Enter group name'
        })

    def get_members_email(self):
        members_email = []
        for name, value in self.cleaned_data.items():
            if name.startswith('member_'):
                members_email.append(value)
        return members_email
