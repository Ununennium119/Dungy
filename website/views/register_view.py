from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from website.forms import UserRegisterForm


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        else:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)
