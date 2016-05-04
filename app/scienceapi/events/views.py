from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from scienceapi.events.models import Event
from scienceapi.events.serializers import (
    EventSerializer,
    EventUserSerializer,
    EventProjectSerializer,
    EventExpandAllSerializer,
)


def serializer_class(self):
        expand = self.request.query_params.get('expand')
        if expand is not None:
            expand = expand.split(',')
            if 'users' in expand and 'projects' not in expand:
                return EventUserSerializer
            elif 'projects' in expand and 'users' not in expand:
                return EventProjectSerializer
            elif 'projects' in expand and 'users' in expand:
                return EventExpandAllSerializer
            else:
                return EventSerializer
        else:
            return EventSerializer


class EventsListView(ListAPIView):
    """
    A view that permits a GET to allow listing all the events
    in the database

    Route - `/events`

    **Query Parameters** -

    - `?expand=` -
    Forces the response to include basic
    information about a relation instead of just
    hyperlinking the relation associated
    with this event.

           Currently supported values are `?expand=users`,
           `?expand=projects` and `?expand=users,projects`

    """
    queryset = Event.objects.all()
    pagination_class = PageNumberPagination
    get_serializer_class = serializer_class


class EventView(RetrieveAPIView):
    """
    A view that permits a GET to allow listing of a single event
    by providing its `id` as a parameter

    Route - `/events/:id`

    **Query Parameters** -

    - `?expand=` -
    Forces the response to include basic
    information about a relation instead of just
    hyperlinking the relation associated
    with this event.

           Currently supported values are `?expand=users`,
           `?expand=projects` and `?expand=users,projects`

    """
    queryset = Event.objects.all()
    pagination_class = None
    get_serializer_class = serializer_class
