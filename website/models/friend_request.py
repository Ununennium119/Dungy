import uuid

from django.db import models

from website.models import User


class FriendRequest(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sent_friend_requests_set')
    receiver = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='received_friend_requests_set')

    def __str__(self):
        return f'Friend request from "{self.sender.username}" to "{self.receiver.username}"'
