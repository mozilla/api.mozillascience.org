import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from urllib.parse import urlencode

from scienceapi.projects.serializers import (
    ProjectSerializer,
    ProjectEventSerializer,
    ProjectExpandAllSerializer,
)
from scienceapi.users.tests.test_models import UserFactory
from scienceapi.events.tests.test_models import EventFactory
from scienceapi.projects.tests.test_models import (
    ProjectFactory,
    ResourceLinkFactory,
    UserProjectFactory,
)


class TestProjectListView(TestCase):

    def create_user_project(self, user, project):
        UserProjectFactory.build(
            project=project,
            user=user,
            role='Lead'
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

    def create_event(self):
        event = EventFactory()
        event.save()
        return event

    def create_project_event(self, project, event):
        project.events.add(event)
        project.save()

    def setUp(self):
        self.projects = self.create_projects()
        self.user = self.create_user()
        self.event = self.create_event()
        for project in self.projects:
            self.create_user_project(
                user=self.user, project=project
            )
        self.create_project_event(
            project=self.projects[0],
            event=self.event,
        )

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

    def test_get_projects_with_expand_leads_query(self):
        """
        Check if we get a list of projects with lead info expanded
        """
        response = self.client.get('{url}?{query}'.format(
            url=reverse('project-list'),
            query=urlencode({'expand': 'leads'}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data['results'][0]['leads'][0]), dict)

    def test_get_project_with_expand_users_query(self):
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

    def test_get_projects_with_expand_events_query(self):
        """
        Check if we get a list of projects with users' info expanded
        """
        response = self.client.get('{url}?{query}'.format(
            url=reverse('project-list'),
            query=urlencode({'expand': 'events'}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        project = ProjectEventSerializer(self.projects[0], context={
            'request': response.wsgi_request
        }).data
        response_project = response_data['results'][
            response_data['results'].index(project)
        ]
        self.assertEqual(
            type(response_project['events'][0]),
            dict,
        )

    def test_get_project_with_expand_events_query(self):
        """
        Check if we get project with users' info expanded
        """
        id = self.projects[0].id
        response = self.client.get('{url}?{query}'.format(
            url=reverse('project', kwargs={'pk': id}),
            query=urlencode({'expand': 'events'}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data['events'][0]), dict)

    def test_get_projects_with_expand_leads_and_events_query(self):
        """
        Check if we get a list of projects with leads' info expanded
        """
        response = self.client.get('{url}?{query}'.format(
            url=reverse('project-list'),
            query=urlencode({'expand': ','.join(('events', 'leads'))}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        project = ProjectExpandAllSerializer(self.projects[0], context={
            'request': response.wsgi_request
        }).data
        response_project = response_data['results'][
            response_data['results'].index(project)
        ]
        self.assertEqual(
            type(response_project['events'][0]),
            dict,
        )
        self.assertEqual(
            type(response_data['results'][0]['leads'][0]),
            dict,
        )

    def test_get_project_with_expand_users_and_events_query(self):
        """
        Check if we get project with users' info expanded
        """
        id = self.projects[0].id
        response = self.client.get('{url}?{query}'.format(
            url=reverse('project', kwargs={'pk': id}),
            query=urlencode({'expand': ','.join(('events', 'users'))}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data['events'][0]), dict)
        self.assertEqual(type(response_data['users'][0]), dict)
