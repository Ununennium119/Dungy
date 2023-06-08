from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from website.forms.profile_edit_form import ProfileForm
from website.models import User


@method_decorator(login_required, name='dispatch')
class ProfileView(SuccessMessageMixin, UpdateView):
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('dashboard')
    success_message = 'Profile edited Successfully!'

    def get_object(self, **kwargs):
        return User.objects.get(id=self.request.user.id)
