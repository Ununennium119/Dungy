from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from website.forms import CostCreationForm, CostUpdateForm
from website.models import Group, CostMember, Cost


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


@method_decorator(login_required, name='dispatch')
class CostUpdateView(SuccessMessageMixin, UpdateView):
    template_name = 'cost/edit-cost.html'
    form_class = CostUpdateForm
    success_message = 'Expense edited successfully!'

    def get_success_url(self):
        group_slug = self.kwargs['group_slug']
        pk = self.kwargs['pk']
        return reverse_lazy('single-cost', kwargs={'group_slug': group_slug, 'pk': pk})

    def get_queryset(self):
        cost_id = self.kwargs['pk']
        cost = Cost.objects.filter(id=cost_id)
        return cost


@method_decorator(login_required, name='dispatch')
class CostDeleteView(SuccessMessageMixin, DeleteView):
    template_name = 'cost/delete-cost.html'
    success_message = 'Expense deleted successfully!'

    def get_success_url(self):
        group_slug = self.kwargs['group_slug']
        return reverse_lazy('single-group', kwargs={'slug': group_slug})

    def get_queryset(self):
        cost_id = self.kwargs['pk']
        cost = Cost.objects.filter(id=cost_id)
        return cost

    def form_valid(self, form):
        for cost_member in self.object.members_set.all():
            cost_member.delete()
        return super(CostDeleteView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class CostDetailView(DetailView):
    model = Cost
    template_name = 'cost/single-cost.html'
