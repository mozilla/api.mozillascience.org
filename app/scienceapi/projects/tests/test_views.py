import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from urllib.parse import urlencode

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
        """
        Check if we can get a list of projects
        """
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
        """
        Check if we can get a single project by its `id`
        """

        id = self.projects[0].id
        response = self.client.get(reverse('project', kwargs={'pk': id}))
        self.assertEqual(response.status_code, 200)

    def test_projects_search_multiple_terms(self):
        """
        Check if we can get a list of projects based on a search
        query containing a comma-separated list of search terms
        """

        response = self.client.get(
            '{url}?{queryparams}'.format(
                url=reverse('project-list'),
                queryparams=urlencode({
                    'search': self.projects[0].name
                })
            )
        )

        self.assertEqual(response.status_code, 200)
        projects_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(projects_data['count'], 1)

    def test_get_projects_with_expand_query(self):
        """
        Check if we get a list of projects with users' info expanded
        """
        response = self.client.get('{url}?{query}'.format(
            url=reverse('project-list'),
            query=urlencode({'expand': 'users'}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data['results'][0]['users'][0]), dict)

    def test_get_project_with_expand_query(self):
        """
        Check if we get project with users' info expanded
        """
        id = self.projects[0].id
        response = self.client.get('{url}?{query}'.format(
            url=reverse('project', kwargs={'pk': id}),
            query=urlencode({'expand': 'users'}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data['users'][0]), dict)
