from django.urls import path
from website.views import RegisterView, LoginView, LogoutView, DashboardView, GroupCreationView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("new-group/", GroupCreationView.as_view(), name='create group'),
]
