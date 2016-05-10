from django.conf.urls import url

from scienceapi.resources.views import ResourcesListView


urlpatterns = [
    url('^$', ResourcesListView.as_view(), name='resource-list'),
]
