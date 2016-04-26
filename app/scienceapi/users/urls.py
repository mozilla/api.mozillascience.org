from django.conf.urls import url

from scienceapi.users.views import (
    UsersListView,
    UserView,
)


urlpatterns = [
    url(r'^$', UsersListView.as_view(), name='user-list'),
    url(r'^(?P<pk>[0-9]+)/', UserView.as_view(), name='user'),
]
