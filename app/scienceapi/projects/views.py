from rest_framework.generics import ListAPIView

from scienceapi.projects.models import Project
from scienceapi.projects.serializers import ProjectWithDetailsSerializer


class ProjectsListView(ListAPIView):
    """
    A view that permits a GET to allow listing all the projects
    in the database
    """
    queryset = Project.objects.all()
    serializer_class = ProjectWithDetailsSerializer
    pagination_class = None
