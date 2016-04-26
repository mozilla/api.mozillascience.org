from django.conf.urls import url

from scienceapi.events.views import EventsListView


urlpatterns = [
    url('^$', EventsListView.as_view(), name='event-list')
]
