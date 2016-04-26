from rest_framework.generics import ListAPIView, RetrieveAPIView

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


class UserView(RetrieveAPIView):
    """
    A view that permits a GET to allow listing of a single user
    by providing their `id` as a parameter

    Route - `/users/:id`
    """
    queryset = User.objects.all()
    serializer_class = UserWithDetailsSerializer
    pagination_class = None
