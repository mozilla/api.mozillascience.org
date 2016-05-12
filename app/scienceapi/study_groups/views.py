from rest_framework.generics import ListAPIView, RetrieveAPIView

from scienceapi.study_groups.models import StudyGroup
from scienceapi.study_groups.serializers import StudyGroupSerializer


class StudyGroupsListView(ListAPIView):
    """
    A view that permits a GET to allow listing all the study groups
    in the database

    Route - `/study-groups`
    """
    queryset = StudyGroup.objects.all()
    pagination_class = None
    serializer_class = StudyGroupSerializer


class StudyGroupView(RetrieveAPIView):
    """
    A view that permits a GET to allow listing of a single study group
    by providing their `id` as a parameter

    Route - `/study-groups/:id`
    """
    queryset = StudyGroup.objects.all()
    pagination_class = None
    serializer_class = StudyGroupSerializer
