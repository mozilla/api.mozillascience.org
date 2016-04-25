from django.conf.urls import url

from scienceapi.users.views import UsersListView


urlpatterns = [
    url('^$', UsersListView.as_view())
]
