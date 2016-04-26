from django.conf.urls import url

from scienceapi.projects.views import (
    ProjectsListView,
    ProjectView,
)


urlpatterns = [
    url('^$', ProjectsListView.as_view(), name='project-list'),
    url(r'^(?P<pk>[0-9]+)/', ProjectView.as_view(), name='project'),
]
