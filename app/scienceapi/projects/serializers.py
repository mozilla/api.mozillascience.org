from rest_framework import serializers

from scienceapi.utility.github import get_contributors
from scienceapi.projects.models import (
    Project,
    ResourceLink,
    Category,
)
from scienceapi.users.models import UserProject
from scienceapi.events.models import Event


class ResourceLinkSerializer(serializers.ModelSerializer):
    """
    Serializes links included in a project by only showing their
    URLS and placeholders
    """
    class Meta:
        model = ResourceLink
        fields = ('url', 'title')


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes a list of categories from the model
    """
    class Meta:
        model = Category


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes a user by including only a few details that
    might be necessary to be known when fetching a project
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


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializes a project with embeded information including
    list of tags, categories and links associated with that project
    as simple strings. It also includes a list of hyperlinks to events
    that are associated with this project as well as hyperlinks to users
    that are involved with the project
    """
    tags = serializers.StringRelatedField(many=True)
    categories = serializers.StringRelatedField(many=True)
    links = ResourceLinkSerializer(many=True)
    users = UserSerializer(
        source='userproject_set',
        many=True,
    )
    events = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='event'
    )

    class Meta:
        model = Project


class ProjectWithGithubSerializer(ProjectSerializer):
    """
    Serializes a project with embeded information including
    list of tags, categories and links associated with that project
    as simple strings. It also includes a list of hyperlinks to events
    that are associated with this project as well as hyperlinks to users
    that are involved with the project and its github contributor list
    """
    github_contributors = serializers.SerializerMethodField()

    def get_github_contributors(self, obj):
        return get_contributors(
            owner=obj.github_owner,
            repository=obj.github_repository,
        )


class EventSerializer(serializers.ModelSerializer):
    """
    Serializes an event by including only a few details that
    might be necessary to be known when fetching a project
    """

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'image_url',
            'slug',
        )


class ProjectEventSerializer(ProjectSerializer):
    """
    Serializes a project with embeded information including
    list of tags, categories and links associated with that project
    as simple strings. It also includes a list of hyperlinks to users
    that are associated with this project and relevant details of every
    event associated with this project
    """

    events = EventSerializer(many=True)


class ProjectUserSerializer(ProjectSerializer):
    """
    Serializes a project with embeded information including
    list of tags, categories and links associated with that project
    as simple strings. It also includes a list of hyperlinks to events
    that are associated with this project and relevant details of every
    user associated with this project
    """

    users = UserSerializer(
        source='userproject_set',
        many=True,
    )


class ProjectExpandAllSerializer(ProjectSerializer):
    """
    Serializes a project with embeded information including
    list of tags, categories and links associated with that project
    as simple strings. It also includes relevant details of every
    user and event associated with this project
    """

    events = EventSerializer(many=True)
    users = UserSerializer(many=True)
