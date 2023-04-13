from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, CreateView, TemplateView

from users.forms import UserRegisterForm, UserLoginForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        else:
            return super(RegisterView, self).dispatch(request, *args, **kwargs)


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                return redirect(request.GET.get("next", "dashboard"))
            messages.error(request, "Username or password is invalid!")

        context = {
            "form": form
        }
        return render(request, "users/login.html", context)


@method_decorator(login_required, name="dispatch")
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "User logged out successfully.")
        return redirect("login")


@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "users/dashboard.html"
