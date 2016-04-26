from rest_framework.generics import ListAPIView

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
    pagination_class = None
