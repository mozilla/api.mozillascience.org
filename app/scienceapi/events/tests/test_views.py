import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from urllib.parse import urlencode

import scienceapi.utility.tests as test_utils
from scienceapi.events.serializers import (
    EventSerializer,
    EventProjectSerializer,
    EventExpandAllSerializer,
)


class TestEventView(TestCase):
    def setUp(self):
        self.projects = test_utils.create_projects()
        self.user = test_utils.create_user()
        self.events = test_utils.create_events()
        for project in self.projects:
            test_utils.create_user_project(
                user=self.user, project=project
            )
        for val in self.events:
            test_utils.create_project_event(
                project=self.projects[0],
                event=self.events[val],
            )
            test_utils.add_attendees(self.user, self.events[val])
            test_utils.add_facilitators(self.user, self.events[val])

    def test_list_events_returns_event_data(self):
        """
        Check if we can get a list of events
        """
        response = self.client.get(reverse('event-list'))

        self.assertEqual(response.status_code, 200)
        event_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(event_data['results']), len(self.events))
        for val in self.events:
            event_serializer = EventSerializer(self.events[val], context={
                'request': response.wsgi_request
            })
            self.assertIn(event_serializer.data, event_data['results'])

    def test_get_single_event_data(self):
        """
        Check if we can get a single event by its `id`
        """

        id = self.events['past'].id
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
        id = self.events['past'].id
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
        event = EventProjectSerializer(self.events['past'], context={
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
        id = self.events['past'].id
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
        event = EventExpandAllSerializer(self.events['past'], context={
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
        id = self.events['past'].id
        response = self.client.get('{url}?{query}'.format(
            url=reverse('event', kwargs={'pk': id}),
            query=urlencode({'expand': ','.join(('projects', 'users'))}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data['projects'][0]), dict)
        self.assertEqual(type(response_data['facilitators'][0]), dict)
        self.assertEqual(type(response_data['attendees'][0]), dict)

    def test_get_future_events(self):
        response = self.client.get('{url}?{query}'.format(
            url=reverse('event-list'),
            query=urlencode({'filter': 'future'}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        event_serializer = EventSerializer(self.events['future'], context={
            'request': response.wsgi_request
        })
        self.assertEqual(len(response_data['results']), 1)
        self.assertIn(event_serializer.data, response_data['results'])

    def test_get_past_events(self):
        response = self.client.get('{url}?{query}'.format(
            url=reverse('event-list'),
            query=urlencode({'filter': 'past'}),
        ))
        response_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        event_serializer = EventSerializer(self.events['past'], context={
            'request': response.wsgi_request
        })
        self.assertEqual(len(response_data['results']), 1)
        self.assertIn(event_serializer.data, response_data['results'])
