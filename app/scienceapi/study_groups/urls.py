from django.conf.urls import url

from scienceapi.study_groups.views import StudyGroupsListView, StudyGroupView


urlpatterns = [
    url('^$', StudyGroupsListView.as_view(), name='studygroup-list'),
    url(r'^(?P<pk>[0-9]+)/', StudyGroupView.as_view(), name='studygroup'),
]
