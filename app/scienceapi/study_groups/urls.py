from django.conf.urls import url

from scienceapi.study_groups.views import StudyGroupsListView


urlpatterns = [
    url('^$', StudyGroupsListView.as_view(), name='studygroup-list'),
]
