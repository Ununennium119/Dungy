from django.urls import path
from website.views import RegisterView, LoginView, LogoutView, DashboardView, GroupCreationView, GroupDetailView, \
    CostCreationView, FriendRequestCreationView, FriendListView, FriendRequestCancelView, FriendRequestAcceptView, \
    FriendRequestRejectView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('friends/', FriendListView.as_view(), name='friends-list'),
    path('friends/new/', FriendRequestCreationView.as_view(), name='add-friend'),
    path('friends/cancel-request/', FriendRequestCancelView.as_view(), name='cancel-friend-request'),
    path('friends/accept-request/', FriendRequestAcceptView.as_view(), name='accept-friend-request'),
    path('friends/reject-request/', FriendRequestRejectView.as_view(), name='reject-friend-request'),
    path('groups/new/', GroupCreationView.as_view(), name='create-group'),
    path('groups/<slug:slug>/', GroupDetailView.as_view(), name='single-group'),
    path('groups/<slug:slug>/costs/new/', CostCreationView.as_view(), name='create-cost'),
]
