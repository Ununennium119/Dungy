from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

from website.forms import GroupCreationForm
from website.models import User


@method_decorator(login_required, name='dispatch')
class GroupCreationView(View):
    template_name = 'create-group.html'
    form_class = GroupCreationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, members_fields_count=request.POST.get('members_fields_count'))
        if form.is_valid():
            group = form.save()
            group.members.add(self.request.user)
            members_email = form.get_members_email()
            for email in members_email:
                try:
                    user = User.objects.get(email=email)
                    group.members.add(user)
                except User.DoesNotExist:
                    continue
            group.save()
            messages.success(request, 'Group created successfully!')
            return redirect('dashboard')

        context = {
            'form': form
        }
        return render(request, self.template_name, context)



