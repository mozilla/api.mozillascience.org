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

    def create_user_project(self, user, project):
        UserProjectFactory.build(
            project=project,
            user=user,
        ).save()

    def create_link(self, project):
        link = ResourceLinkFactory.build(project=project)
        link.save()

    def create_projects(self):
        projects = [ProjectFactory() for i in range(3)]
        for project in projects:
            project.save()
            self.create_link(project)
        return projects

    def create_user(self):
        user = UserFactory()
        user.save()
        return user

    def setUp(self):
        self.projects = self.create_projects()
        self.user = self.create_user()
        for project in self.projects:
            self.create_user_project(user=self.user, project=project)

    def test_list_projects_returns_project_data(self):
        response = self.client.get(reverse('project-list'))

        self.assertEqual(response.status_code, 200)
        projects_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(projects_data['results']), len(self.projects))
        for project in self.projects:
            project_serializer = ProjectSerializer(project, context={
                'request': response.wsgi_request
            })
            self.assertIn(project_serializer.data, projects_data['results'])

    def test_get_single_project_data(self):
        id = self.projects[0].id
        response = self.client.get(reverse('project', kwargs={'pk': id}))
        self.assertEqual(response.status_code, 200)
