from rest_framework.generics import ListAPIView

from scienceapi.users.models import User
from scienceapi.users.serializers import UserWithDetailsSerializer


class UsersListView(ListAPIView):
    """
    A view that permits a GET to allow listing all the users
    in the database

    Route - `/users`
    """
    queryset = User.objects.all()
    serializer_class = UserWithDetailsSerializer
    pagination_class = None
