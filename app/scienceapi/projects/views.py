import django_filters
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import filters

from scienceapi.projects.models import Project, Category
from scienceapi.projects.serializers import (
    ProjectWithDetailsSerializer,
    CategorySerializer,
    ProjectWithDetailsExpandUserSerializer,
    ProjectWithDetailsExpandEventSerializer,
    ProjectWithDetailsExpandAllSerializer,
)


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

    **Route** - `/projects`

    **Query Parameters** -

    - `?search=` - Allows search terms
    - `?sort=` - Allows sorting of projects.
        - date_created - `?sort=date_created`
        - date_updated - `?sort=date_updated`

        *To sort in descending order, prepend the field with a '-', for e.g.
        `?sort=-date_updated`*

    - `?tags=` - Allows filtering projects by a specific tag
    - `?categories=` - Allows filtering projects by a specific category
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


class ProjectView(RetrieveAPIView):
    """
    A view that permits a GET to allow listing of a single project
    by providing its `id` as a parameter

    Route - `/projects/:id`

    Query Parameters -
        * `?expandusers` - Forces the response to include basic
                           user information instead of just
                           hyperlinking the list of users associated
                           with this project
    """
    queryset = Project.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        expand = self.request.query_params.get('expand')
        if expand is not None:
            expand = expand.split(',')
            if 'users' in expand and 'events' not in expand:
                return ProjectWithDetailsExpandUserSerializer
            elif 'events' in expand and 'users' not in expand:
                return ProjectWithDetailsExpandEventSerializer
            elif 'events' in expand and 'users' in expand:
                return ProjectWithDetailsExpandAllSerializer
            else:
                return ProjectWithDetailsSerializer
        else:
            return ProjectWithDetailsSerializer


class CategoryListView(ListAPIView):
    """
    A view that permits a GET to allow listing of all categories
    in the database
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
