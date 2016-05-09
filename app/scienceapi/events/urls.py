from django.conf.urls import url

from scienceapi.events.views import (
    EventsListView,
    EventView,
    EventSlugView,
)


urlpatterns = [
    url('^$', EventsListView.as_view(), name='event-list'),
    url(r'^(?P<pk>[0-9]+)/', EventView.as_view(), name='event'),
    url(r'^(?P<slug>[-\w]+)/', EventSlugView.as_view(), name='event-slug'),
]
