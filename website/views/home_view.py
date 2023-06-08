from django.views.generic import TemplateView
from website.models import User, Group, Transaction, Cost


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            "users_count": User.objects.all().count(),
            "groups_count": Group.objects.all().count(),
            "transactions": Transaction.objects.all().count(),
            "costs": Cost.objects.all().count()
        }
