from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from website.models import User, Cost


@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.user.id)

        context['username'] = user.username
        context['groups'] = user.group_set.all().prefetch_related('costs_set')
        if user.debt and user.credit:
            context['owe'] = user.debt
            context['owed'] = user.credit
            context['total_balance'] = context['owed'] - context['owe']
        else:
            context['owe'] = 0.0
            context['owed'] = 0.0
            context['total_balance'] = 0.0
        context['owe_costs'] = Cost.objects.filter(members_set__user=user, members_set__paid=False)
        context['owed_costs'] = user.paid_costs.filter(members_set__paid=False)

        return context
