from rest_framework import serializers

from scienceapi.users.models import User


class UserWithDetailsSerializer(serializers.ModelSerializer):
    """
    Serializes a list of users with data including the list of projects
    that the user created.
    """
    projects = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='project'
    )

    class Meta:
        model = User
        fields = '__all__'
