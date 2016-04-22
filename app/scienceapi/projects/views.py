import django_filters
from rest_framework.generics import ListAPIView
from rest_framework import filters

from scienceapi.projects.models import Project
from scienceapi.projects.serializers import ProjectWithDetailsSerializer


class ProjectSearchFilter(filters.SearchFilter):
    """
    We use a custom search filter to search based on a query
    like so - `?search=my_search_term`
    """
    def get_search_terms(self, request):
        params = request.query_params.get(self.search_param, '')
        return params.split(',')


class ProjectCustomFilter(filters.FilterSet):
    """
    We add custom filtering to allow you to filter by:
        * Category - pass the `?categories=` query parameter
        * Tag - pass the `?tags=` query parameter
    Both accept only one filter value i.e. one tag and/or one
    category.
    """
    tags = django_filters.CharFilter(
        name='tags__name',
        lookup_expr='iexact',
    )
    categories = django_filters.CharFilter(
        name='categories__name',
        lookup_expr='iexact',
    )

    class Meta:
        model = Project
        fields = ['tags', 'categories']


class ProjectsListView(ListAPIView):
    """
    A view that permits a GET to allow listing all the projects
    in the database
    """
    queryset = Project.objects.all()
    serializer_class = ProjectWithDetailsSerializer
    pagination_class = None
    filter_backends = (
        filters.DjangoFilterBackend,
        ProjectSearchFilter,
        filters.OrderingFilter,
    )
    filter_class = ProjectCustomFilter
    ordering_fields = (
        'date_created',
        'date_updated',
    )
    search_fields = (
        'name',
        '=institution',
        'description',
        'short_description',
        '=license',
        '=tags__name',
        '=categories__name',
    )
