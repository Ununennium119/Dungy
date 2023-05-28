from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from website.forms import FriendRequestCreationForm
from website.models import User, FriendRequest


@method_decorator(login_required, name='dispatch')
class FriendRequestCreationView(FormView):
    template_name = 'friend/create-friend-request.html'
    form_class = FriendRequestCreationForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {}
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'No user with this email exists!')
            else:
                if user.id == self.request.user.id:
                    messages.error(request, 'You can\'t send a friend request to yourself!')
                else:
                    friend_request = FriendRequest(sender_id=self.request.user.id, receiver_id=user.id)
                    friend_request.save()
                    messages.success(request, 'Friend request sent successfully!')
                    return redirect('dashboard')

        context['form'] = form
        return render(request, self.template_name, context)
