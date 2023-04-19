from django.urls import path
from website.views import GroupCreationView

urlpatterns = [
    path("new-group/", GroupCreationView.as_view(), name='create group'),
]
