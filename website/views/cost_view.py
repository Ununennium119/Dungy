from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from website.forms import CostCreationForm
from website.models import Group, CostMember


@method_decorator(login_required, name='dispatch')
class CostCreationView(SuccessMessageMixin, CreateView):
    template_name = 'cost/create-cost.html'
    form_class = CostCreationForm
    success_message = 'Expense added successfully!'

    def post(self, request, *args, **kwargs):
        group = self.get_queryset()
        form = self.form_class(request.POST, group=group)
        if form.is_valid():
            cost = form.save(commit=False)
            cost.group = group
            cost.save()

            members = form.cleaned_data['members']
            for member in members:
                cost_member = CostMember(user=member, cost=cost)
                cost_member.save()
            messages.success(request, self.success_message)
            return redirect(self.get_success_url())

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def get_success_url(self):
        slug = self.kwargs['slug']
        return reverse_lazy('single-group', kwargs={'slug': slug})

    def get_queryset(self):
        group = get_object_or_404(Group, slug=self.kwargs['slug'])
        if not group.members.filter(id=self.request.user.id).exists():
            raise PermissionDenied()
        return group

    def get_form_kwargs(self):
        kwargs = super(CostCreationView, self).get_form_kwargs()
        kwargs['group'] = self.get_queryset()
        return kwargs

    def form_valid(self, form):
        form.instance.group = self.get_queryset()
        return super(CostCreationView, self).form_valid(form)
