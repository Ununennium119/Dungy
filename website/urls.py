from django.urls import path
from website.views import RegisterView, LoginView, LogoutView, DashboardView, GroupCreationView, GroupDetailView, CostCreationView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('groups/new/', GroupCreationView.as_view(), name='create-group'),
    path('groups/<slug:slug>/', GroupDetailView.as_view(), name='single-group'),
    path('groups/<slug:slug>/costs/new/', CostCreationView.as_view(), name='create-cost')
]
