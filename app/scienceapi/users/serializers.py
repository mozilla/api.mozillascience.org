from rest_framework import serializers

from scienceapi.users.models import User


class UserWithDetailsSerializer(serializers.ModelSerializer):
    """
    Serializes a user with data including the list of projects
    that the user created.
    """
    projects = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='project'
    )
    events_created = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='event'
    )
    events_attended = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='event'
    )
    events_facilitated = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='event'
    )

    class Meta:
        model = User
        fields = '__all__'
