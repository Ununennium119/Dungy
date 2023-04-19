from rest_framework.serializers import ModelSerializer

from website.models import Group


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
