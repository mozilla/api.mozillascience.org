from django.conf.urls import url

from scienceapi.resources.views import ResourcesListView, ResourceView


urlpatterns = [
    url('^$', ResourcesListView.as_view(), name='resource-list'),
    url(r'^(?P<pk>[0-9]+)/', ResourceView.as_view(), name='resource'),
]
