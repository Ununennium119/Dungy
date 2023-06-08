from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from website.forms import IncreaseBalanceForm
from website.models import User


@method_decorator(login_required, name='dispatch')
class IncreaseBalanceView(SuccessMessageMixin, FormView):
    template_name = 'increase-balance.html'
    form_class = IncreaseBalanceForm
    success_url = reverse_lazy('dashboard')
    success_message = 'Balance increased successfully!'

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        user = User.objects.get(id=self.request.user.id)
        user.balance += amount
        user.save()

        return redirect('dashboard')
