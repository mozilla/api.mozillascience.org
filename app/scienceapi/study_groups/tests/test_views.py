import json
from django.core.urlresolvers import reverse
from django.test import TestCase

from scienceapi.study_groups.serializers import StudyGroupSerializer
from scienceapi.study_groups.tests.test_models import StudyGroupFactory


class TestStudyGroupView(TestCase):

    def setUp(self):
        self.study_groups = [StudyGroupFactory() for i in range(3)]
        for study_group in self.study_groups:
            study_group.save()

    def test_list_study_groups_returns_study_group_data(self):
        """
        Check if we can get a list of study groups
        """
        response = self.client.get(reverse('studygroup-list'))

        self.assertEqual(response.status_code, 200)
        study_group_data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(
            len(study_group_data['results']),
            len(self.study_groups)
        )
        for study_group in self.study_groups:
            study_group_serializer = StudyGroupSerializer(
                study_group,
                context={'request': response.wsgi_request}
            )
            self.assertIn(
                study_group_serializer.data,
                study_group_data['results']
            )

    def test_get_single_study_group_data(self):
        """
        Check if we can get a single study group by its `id`
        """

        id = self.study_groups[0].id
        response = self.client.get(reverse('studygroup', kwargs={'pk': id}))
        self.assertEqual(response.status_code, 200)
