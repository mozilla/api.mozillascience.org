from django.conf.urls import url

from scienceapi.projects.views import ProjectsListView


urlpatterns = [
    url('^$', ProjectsListView.as_view())
]
