from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from scienceapi.events.models import Event
from scienceapi.events.serializers import EventWithDetailsSerializer


class EventsListView(ListAPIView):
    """
    A view that permits a GET to allow listing all the events
    in the database

    Route - `/events`
    """
    queryset = Event.objects.all()
    serializer_class = EventWithDetailsSerializer
    pagination_class = PageNumberPagination


class EventView(RetrieveAPIView):
    """
    A view that permits a GET to allow listing of a single event
    by providing its `id` as a parameter

    Route - `/events/:id`
    """
    queryset = Event.objects.all()
    serializer_class = EventWithDetailsSerializer
    pagination_class = None
