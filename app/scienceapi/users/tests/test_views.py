import json
from django.core.urlresolvers import reverse
from django.test import TestCase

from scienceapi.users.serializers import UserWithDetailsSerializer
from scienceapi.users.tests.test_models import UserFactory


class TestUserView(TestCase):

    def setUp(self):
        self.users = [UserFactory() for i in range(3)]
        for user in self.users:
            user.save()

    def test_list_users_returns_user_data(self):
        """
        Check if we can get a list of users
        """
        response = self.client.get(reverse('user-list'))

        self.assertEqual(response.status_code, 200)
        user_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            len(user_data['results']),
            len(self.users)
        )
        for user in self.users:
            user_serializer = UserWithDetailsSerializer(
                user,
                context={'request': response.wsgi_request}
            )
            self.assertIn(
                user_serializer.data,
                user_data['results']
            )

    def test_get_single_user_data(self):
        """
        Check if we can get a single user by its `id`
        """

        id = self.users[0].id
        response = self.client.get(reverse('user', kwargs={'pk': id}))
        self.assertEqual(response.status_code, 200)
