from rest_framework import serializers

from scienceapi.events.models import Event
from scienceapi.projects.models import Project
from scienceapi.utility.common_serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    """
    Serializes an event with each event including the
    list of projects associated with the event and the users attending
    and facilitating the event
    """
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


class ProjectsForEventSerializer(serializers.ModelSerializer):
    """
    Serializes a project used in an event by including most details
    that might be necessary to be known when included as a relation
    in another object set.
    """

    tags = serializers.StringRelatedField(many=True)
    categories = serializers.StringRelatedField(many=True)
    leads = serializers.SerializerMethodField()

    def get_leads(self, project):
        return UserSerializer(
            instance=project.users.filter(
                userproject__role='Lead',
            ),
            many=True
        ).data

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'slug',
            'image_url',
            'institution',
            'short_description',
            'tags',
            'categories',
            'leads',
        )


class EventProjectSerializer(EventSerializer):
    """
    Serializes an event including a list of hyperlinks to users
    that are facilitating or attending this event along with
    relevant details of every project associated with this event
    """

    projects = ProjectsForEventSerializer(many=True)


class EventUserSerializer(EventSerializer):
    """
    Serializes an event including a list of hyperlinks to projects
    associated with this event along with relevant details of every
    user facilitating or attending this event
    """

    attendees = UserSerializer(many=True)
    facilitators = UserSerializer(many=True)


class EventExpandAllSerializer(EventSerializer):
    """
    Serializes an event including relevant details of every project
    associated with this event as well as relevant details of every
    user facilitating or attending this event
    """

    projects = ProjectsForEventSerializer(many=True)
    attendees = UserSerializer(many=True)
    facilitators = UserSerializer(many=True)
