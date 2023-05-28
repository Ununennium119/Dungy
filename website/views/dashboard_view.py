from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


@method_decorator(login_required, name="dispatch")
class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        context['groups'] = self.request.user.group_set.all().prefetch_related('costs_set')
        context['owe'] = 12
        context['owed'] = 2
        context['total_balance'] = context['owe'] + context['owed']
        return context
