from rest_framework.generics import ListAPIView

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
