from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, TemplateView

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
                receiver_user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'No user with this email exists!')
            else:
                if receiver_user.id == self.request.user.id:
                    messages.error(request, 'You cannot send a friend request to yourself!')
                else:
                    user = User.objects.get(id=self.request.user.id)
                    if user.friends.filter(id=receiver_user.id).exists():
                        messages.error(request, 'You cannot send a friend request to your friend!')
                    elif user.sent_friend_requests_set.filter(receiver_id=receiver_user.id).exists():
                        messages.error(request, 'You already have sent a friend request to this user!')
                    else:
                        friend_request = FriendRequest(sender_id=self.request.user.id, receiver_id=receiver_user.id)
                        friend_request.save()
                        messages.success(request, 'Friend request sent successfully!')
                        return redirect('friends-list')

        context['form'] = form
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class FriendListView(TemplateView):
    template_name = 'friend/friend-list.html'

    def get_context_data(self, **kwargs):
        context = super(FriendListView, self).get_context_data(**kwargs)

        user = User.objects.get(id=self.request.user.id)
        context['friends'] = user.friends.all()
        context['sent_friend_requests'] = user.sent_friend_requests_set.all()
        context['received_friend_requests'] = user.received_friend_requests_set.all()
        return context


@method_decorator(login_required, name='dispatch')
class FriendRequestCancelView(View):
    http_method_names = ['post']

    def post(self, request):
        receiver_username = self.request.POST.get('username')
        try:
            friend_request = self.request.user.sent_friend_requests_set.get(receiver__username=receiver_username)
        except FriendRequest.DoesNotExist:
            messages.error(request, 'Cannot cancel friend request!')
            return redirect('friends-list')

        friend_request.delete()
        messages.success(request, 'Friend request canceled successfully!')
        return redirect('friends-list')


@method_decorator(login_required, name='dispatch')
class FriendRequestAcceptView(View):
    http_method_names = ['post']

    def post(self, request):
        user = User.objects.get(id=self.request.user.id)
        sender_username = self.request.POST.get('username')
        try:
            friend_request = user.received_friend_requests_set.get(sender__username=sender_username)
            sender = friend_request.sender
        except FriendRequest.DoesNotExist:
            messages.error(request, 'Cannot accept friend request!')
            return redirect('friends-list')

        friend_request.delete()
        try:
            friend_request = user.sent_friend_requests_set.get(receiver__username=sender_username)
            friend_request.delete()
        except FriendRequest.DoesNotExist:
            pass

        sender.friends.add(user)
        user.friends.add(sender)

        messages.success(request, 'Friend request accepted successfully!')
        return redirect('friends-list')


@method_decorator(login_required, name='dispatch')
class FriendRequestRejectView(View):
    http_method_names = ['post']

    def post(self, request):
        user = self.request.user
        sender_username = self.request.POST.get('username')
        try:
            friend_request = user.received_friend_requests_set.get(sender__username=sender_username)
        except FriendRequest.DoesNotExist:
            messages.error(request, 'Cannot reject friend request!')
            return redirect('friends-list')

        friend_request.delete()

        messages.success(request, 'Friend request rejected successfully!')
        return redirect('friends-list')
