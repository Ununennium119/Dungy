from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from website.models import User


@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = User.objects.get(id=self.request.user.id)
        context['username'] = user.username
        context['groups'] = user.group_set.all().prefetch_related('costs_set')
        context['owe'] = user.debt
        context['owed'] = user.credit
        context['total_balance'] = context['owed'] - context['owe']
        return context
