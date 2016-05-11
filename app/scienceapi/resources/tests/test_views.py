import json
from django.core.urlresolvers import reverse
from django.test import TestCase

from scienceapi.resources.serializers import ResourceSerializer
from scienceapi.resources.tests.test_models import ResourceFactory


class TestResourceView(TestCase):

    def setUp(self):
        self.resources = [ResourceFactory() for i in range(3)]
        for resource in self.resources:
            resource.save()

    def test_list_resources_returns_resource_data(self):
        """
        Check if we can get a list of resources
        """
        response = self.client.get(reverse('resource-list'))

        resource_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(resource_data['results']), len(self.resources))
        for resource in self.resources:
            resource_serializer = ResourceSerializer(resource, context={
                'request': response.wsgi_request
            })
            self.assertIn(resource_serializer.data, resource_data['results'])

    def test_get_single_resource_data(self):
        """
        Check if we can get a single resource by its `id`
        """

        id = self.resources[0].id
        response = self.client.get(reverse('resource', kwargs={'pk': id}))
        self.assertEqual(response.status_code, 200)
