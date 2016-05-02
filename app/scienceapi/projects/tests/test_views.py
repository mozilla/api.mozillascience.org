import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from scienceapi.projects.serializers import ProjectSerializer
from scienceapi.projects.tests.test_models import (
    UserFactory,
    ProjectFactory,
    ResourceLinkFactory,
    UserProjectFactory,
)


class TestProjectListView(TestCase):

    def test_list_projects_returns_project_data(self):
        user = UserFactory()
        user.save()
        project = ProjectFactory()
        project.save()
        link = ResourceLinkFactory.build(
            project=project,
        )
        link.save()
        user_project = UserProjectFactory.build(
            project=project,
            user=user,
        )
        user_project.save()

        response = self.client.get(reverse('project-list'))

        self.assertEqual(response.status_code, 200)
        projects_data = json.loads(response.content.decode('utf-8'))

        project_serializer = ProjectSerializer(project, context={
            'request': response.wsgi_request
        })
        self.assertIn(project_serializer.data, projects_data)
