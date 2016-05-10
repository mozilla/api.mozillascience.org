import django_filters

from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from scienceapi.resources.models import Resource
from scienceapi.resources.serializers import ResourceSerializer


class ResourceCustomFilter(filters.FilterSet):
    """
    We add custom filtering to allow you to filter by:
        * Tag - pass the `?tags=` query parameter
    It accepts only one filter tag
    """
    tags = django_filters.CharFilter(
        name='tags__name',
        lookup_expr='iexact',
    )

    class Meta:
        model = Resource
        fields = ['tags']


class ResourceView(RetrieveAPIView):
    """
    A view that permits a GET to allow listing of a single resource
    by providing their `id` as a parameter

    Route - `/resources/:id`
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    pagination_class = None


class ResourcesListView(ListAPIView):
    """
    A view that permits a GET to allow listing all the resources
    in the database

    **Route** - `/resources`

    """
    serializer_class = ResourceSerializer
    pagination_class = PageNumberPagination
    queryset = Resource.objects.all()
    filter_class = ResourceCustomFilter
    filter_backends = (
        filters.DjangoFilterBackend,
    )
