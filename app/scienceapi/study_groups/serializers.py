from rest_framework import serializers

from scienceapi.study_groups.models import StudyGroup


class StudyGroupSerializer(serializers.ModelSerializer):
    """
    Serializes a study group
    """

    class Meta:
        model = StudyGroup
