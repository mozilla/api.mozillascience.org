from rest_framework import serializers

from scienceapi.events.models import Event


class EventWithDetailsSerializer(serializers.ModelSerializer):
    """
    Serializes a list of events with each event including the
    list of projects associated with the event and the users attending
    and facilitating the event
    """
    created_by = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user'
    )
    attendees = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='user'
    )
    facilitators = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='user'
    )
    projects = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='project'
    )

    class Meta:
        model = Event
        fields = '__all__'
