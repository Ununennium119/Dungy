from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, FormView

from website.forms.profile_edit_form import ProfileForm
from website.models import User


class ProfileView(FormView):
    template_name = 'profile.html'
    form_class = ProfileForm

    def get_context_data(self, **kwargs):
        form = self.form_class()
        user = User.objects.get(id=self.request.user.id)
        form.fields['username'].initial = user.username
        form.fields['email'].initial = user.email
        return {"user": user, "form": form}

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {}
        if form.is_valid():
            #todo: complete here to edit profile data
            context['error'] = "Username or password is invalid!"
            messages.error(request, "Username or password is invalid!")

        context['form'] = form
        return render(request, "login.html", context)
