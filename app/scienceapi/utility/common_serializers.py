from rest_framework import serializers

from scienceapi.users.models import UserProject
from scienceapi.events.models import Event


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes a user by including only a few details that
    might be necessary to be known when included as a relation
    in another object set.
    """
    id = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    github_username = serializers.ReadOnlyField(source='user.github_username')
    avatar_url = serializers.ReadOnlyField(source='user.avatar_url')

    class Meta:
        model = UserProject
        fields = (
            'id',
            'username',
            'github_username',
            'avatar_url',
            'role',
        )


class EventSerializer(serializers.ModelSerializer):
    """
    Serializes an event by including only a few details that
    might be necessary to be known when included as a relation
    in another object set.
    """

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'image_url',
            'slug',
        )
