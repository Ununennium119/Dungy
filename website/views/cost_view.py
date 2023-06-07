from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from website.forms import CostCreationForm, CostUpdateForm
from website.models import Group, CostMember, Cost, User
from website.models.transaction import Transaction


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
                cost_member = CostMember(user=member, cost=cost, paid=cost.paid_by.username == member.username)
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

    def get_context_data(self, **kwargs):
        context = super(CostDetailView, self).get_context_data(**kwargs)
        try:
            cost_member = self.object.members_set.get(user=self.request.user)
            context['is_paid'] = cost_member.paid
        except CostMember.DoesNotExist:
            context['is_paid'] = True

        return context


@method_decorator(login_required, name='dispatch')
class CostConfirmPaymentView(DetailView):
    model = Cost
    template_name = 'cost/confirm-cost-payment.html'

    def get_context_data(self, **kwargs):
        context = super(CostConfirmPaymentView, self).get_context_data(**kwargs)
        context['amount'] = self.object.amount / self.object.members_set.count()
        return context


@method_decorator(login_required, name='dispatch')
class CostPay(View):
    def get(self, *args, **kwargs):
        group_slug = kwargs['group_slug']
        cost_id = kwargs['pk']
        user = User.objects.get(id=self.request.user.id)

        cost = get_object_or_404(Cost, id=cost_id)
        cost_members = cost.members_set.all()
        cost_member = cost_members.filter(user=user)
        if not cost_member.exists():
            messages.error(self.request, 'Failed to pay expense!')
            return redirect('single-cost', group_slug=group_slug, pk=cost_id)

        cost_member = cost_members.first()
        if cost_member.paid:
            messages.error(self.request, 'Expense is already paid!')
            return redirect('single-cost', group_slug=group_slug, pk=cost_id)

        amount = cost.amount / cost_members.count()
        if amount > user.balance:
            messages.error(self.request, 'Your balance is not enough!')
            return redirect('single-cost', group_slug=group_slug, pk=cost_id)
        user.balance -= amount
        user.save()

        payer = cost.paid_by
        payer.balance += amount
        payer.save()

        transaction = Transaction(from_user=user, to_user=payer, amount=amount)
        transaction.save()

        cost_member.paid = True
        cost_member.save()

        messages.success(self.request, 'Expense paid successfully!')
        return redirect('single-cost', group_slug=group_slug, pk=cost_id)
