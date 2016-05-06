import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from urllib.parse import urlencode

from scienceapi.events.serializers import (
    EventSerializer,
    EventProjectSerializer,
    EventExpandAllSerializer,
)
from scienceapi.users.tests.test_models import UserFactory
from scienceapi.events.tests.test_models import EventFactory
from scienceapi.projects.tests.test_models import (
    ProjectFactory,
    UserProjectFactory,
)


class TestEventView(TestCase):

    def create_user_project(self, user, project):
        UserProjectFactory.build(
            project=project,
            user=user,
        ).save()

    def create_projects(self):
        projects = [ProjectFactory() for i in range(3)]
        for project in projects:
            project.save()
        return projects

    def create_user(self):
        user = UserFactory()
        user.save()
        return user

    def create_event(self):
        events = [EventFactory() for i in range(3)]
        for event in events:
            event.save()
        return events

    def create_project_event(self, project, event):
        project.events.add(event)
        project.save()

    def add_attendees(self, user, event):
        event.attendees.add(user)
        event.save()

    def add_facilitators(self, user, event):
        event.facilitators.add(user)
        event.save()

    def setUp(self):
        self.projects = self.create_projects()
        self.user = self.create_user()
        self.events = self.create_event()
        for project in self.projects:
            self.create_user_project(
                user=self.user, project=project
            )
        for event in self.events:
            self.create_project_event(
                project=self.projects[0],
                event=event,
            )
            self.add_attendees(self.user, event)
            self.add_facilitators(self.user, event)

    def test_list_events_returns_event_data(self):
        """
        Check if we can get a list of events
        """
        response = self.client.get(reverse('event-list'))

        self.assertEqual(response.status_code, 200)
        event_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(event_data['results']), len(self.events))
        for event in self.events:
            event_serializer = EventSerializer(event, context={
                'request': response.wsgi_request
            })
            self.assertIn(event_serializer.data, event_data['results'])

    def test_get_single_event_data(self):
        """
        Check if we can get a single event by its `id`
        """

        id = self.events[0].id
        response = self.client.get(reverse('event', kwargs={'pk': id}))
        self.assertEqual(response.status_code, 200)

    def test_get_events_with_expand_users_query(self):
        """
        Check if we get a list of events with users' info expanded
        """
        response = self.client.get('{url}?{query}'.format(
            url=reverse('event-list'),
            query=urlencode({'expand': 'users'}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            type(response_data['results'][0]['attendees'][0]),
            dict,
        )
        self.assertEqual(
            type(response_data['results'][0]['facilitators'][0]),
            dict,
        )

    def test_get_event_with_expand_users_query(self):
        """
        Check if we get event with users' info expanded
        """
        id = self.events[0].id
        response = self.client.get('{url}?{query}'.format(
            url=reverse('event', kwargs={'pk': id}),
            query=urlencode({'expand': 'users'}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data['attendees'][0]), dict)
        self.assertEqual(type(response_data['facilitators'][0]), dict)

    def test_get_events_with_expand_projects_query(self):
        """
        Check if we get a list of events with users' info expanded
        """
        response = self.client.get('{url}?{query}'.format(
            url=reverse('event-list'),
            query=urlencode({'expand': 'projects'}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        event = EventProjectSerializer(self.events[0], context={
            'request': response.wsgi_request
        }).data
        response_event = response_data['results'][
            response_data['results'].index(event)
        ]
        self.assertEqual(
            type(response_event['projects'][0]),
            dict,
        )

    def test_get_event_with_expand_projects_query(self):
        """
        Check if we get event with users' info expanded
        """
        id = self.events[0].id
        response = self.client.get('{url}?{query}'.format(
            url=reverse('event', kwargs={'pk': id}),
            query=urlencode({'expand': 'projects'}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data['projects'][0]), dict)

    def test_get_events_with_expand_users_and_projects_query(self):
        """
        Check if we get a list of events with users' info expanded
        """
        response = self.client.get('{url}?{query}'.format(
            url=reverse('event-list'),
            query=urlencode({'expand': ','.join(('projects', 'users'))}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        event = EventExpandAllSerializer(self.events[0], context={
            'request': response.wsgi_request
        }).data
        response_event = response_data['results'][
            response_data['results'].index(event)
        ]
        self.assertEqual(
            type(response_event['projects'][0]),
            dict,
        )
        self.assertEqual(
            type(response_data['results'][0]['attendees'][0]),
            dict,
        )
        self.assertEqual(
            type(response_data['results'][0]['facilitators'][0]),
            dict,
        )

    def test_get_event_with_expand_users_and_projects_query(self):
        """
        Check if we get event with users' info expanded
        """
        id = self.events[0].id
        response = self.client.get('{url}?{query}'.format(
            url=reverse('event', kwargs={'pk': id}),
            query=urlencode({'expand': ','.join(('projects', 'users'))}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data['projects'][0]), dict)
        self.assertEqual(type(response_data['facilitators'][0]), dict)
        self.assertEqual(type(response_data['attendees'][0]), dict)
