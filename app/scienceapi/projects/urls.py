from django.conf.urls import url

from scienceapi.projects.views import (
    ProjectsListView,
    ProjectView,
    CategoryListView,
    ProjectSlugView,
)


urlpatterns = [
    url('^$', ProjectsListView.as_view(), name='project-list'),
    url(r'^categories/', CategoryListView.as_view(), name='category-list'),
    url(r'^(?P<pk>[0-9]+)/', ProjectView.as_view(), name='project'),
    url(r'^(?P<slug>[\w-]+)/', ProjectSlugView.as_view(), name='project-slug'),
]
