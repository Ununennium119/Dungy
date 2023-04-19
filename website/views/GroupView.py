from rest_framework.generics import CreateAPIView
from website.serializers import GroupSerializer


class GroupCreationView(CreateAPIView):
    serializer_class = GroupSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, args, kwargs)
