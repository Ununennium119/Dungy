from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import FormView

from website.forms import UserLoginForm


class LoginView(FormView):
    template_name = "login.html"
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {}
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                return redirect(request.GET.get("next", "dashboard"))
            context['error'] = "Username or password is invalid!"
            messages.error(request, "Username or password is invalid!")

        context['form'] = form.cleaned_data
        return render(request, "login.html", context)
