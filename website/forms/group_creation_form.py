from django import forms

from website.models import Group


class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'type', 'image']
        labels = {'name': 'GROUP NAME', 'type': 'GROUP TYPE', 'image': ''}

    def __init__(self, *args, **kwargs):
        super(GroupCreationForm, self).__init__(*args, **kwargs)

        for i in range(3):
            self.fields[f'member_{i}'] = forms.EmailField(label='', required=False)

    def get_members_email(self):
        members_email = []
        for name, value in self.cleaned_data.items():
            if name.startswith('member_'):
                members_email.append(value)
        return members_email
