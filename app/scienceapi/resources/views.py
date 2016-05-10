from rest_framework.generics import ListAPIView

from scienceapi.resources.models import Resource
from scienceapi.resources.serializers import ResourceSerializer


class ResourcesListView(ListAPIView):
    """
    A view that permits a GET to allow listing all the resources
    in the database

    **Route** - `/resources`

    """
    serializer_class = ResourceSerializer
    pagination_class = None
    queryset = Resource.objects.all()
