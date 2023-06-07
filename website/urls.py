from django.urls import path
from website.views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
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
    path('groups/<slug:group_slug>/costs/<uuid:pk>/', CostDetailView.as_view(), name='single-cost'),
    path('groups/<slug:group_slug>/costs/<uuid:pk>/edit/', CostUpdateView.as_view(), name='edit-cost'),
    path('groups/<slug:group_slug>/costs/<uuid:pk>/delete/', CostDeleteView.as_view(), name='delete-cost'),
    path('groups/<slug:group_slug>/costs/<uuid:pk>/confirm-payment/', CostConfirmPaymentView.as_view(),
         name='confirm-cost-payment'),
    path('groups/<slug:group_slug>/costs/<uuid:pk>/pay/', CostPay.as_view(),
         name='pay-cost'),
]
