from rest_framework import serializers

from scienceapi.utility.github import get_contributors
from scienceapi.utility.common_serializers import (
    UserProjectSerializer,
    EventSerializer,
    ProjectLeads,
)
from scienceapi.projects.models import (
    Project,
    ResourceLink,
    Category,
)


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
        fields = '__all__'


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
    users = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='user'
    )
    events = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='event'
    )

    class Meta:
        model = Project
        fields = '__all__'


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


class ProjectEventSerializer(ProjectSerializer):
    """
    Serializes a project with embeded information including
    list of tags, categories and links associated with that project
    as simple strings. It also includes a list of hyperlinks to users
    that are associated with this project and relevant details of every
    event associated with this project
    """

    events = EventSerializer(many=True)


class ProjectEventWithGithubSerializer(ProjectWithGithubSerializer):
    """
    Serializes a project with embeded information including
    list of tags, categories and links associated with that project
    as simple strings. It also includes a list of hyperlinks to users
    that are associated with this project and relevant details of every
    event associated with this project and its github contributor list
    """

    events = EventSerializer(many=True)


class ProjectLeadSerializer(ProjectSerializer, ProjectLeads):
    """
    Serializes a project with embeded information including
    list of tags, categories and links associated with that project
    as simple strings. It also includes a list of hyperlinks to events
    that are associated with this project and relevant details of every
    user who is a Lead associated with this project
    """
    leads = serializers.SerializerMethodField()

    class Meta:
        model = Project
        exclude = ['users']


class ProjectUserWithGithubSerializer(ProjectWithGithubSerializer):
    """
    Serializes a project with embeded information including
    list of tags, categories and links associated with that project
    as simple strings. It also includes a list of hyperlinks to events
    that are associated with this project and relevant details of every
    user associated with this project and its github contributor list
    """
    users = UserProjectSerializer(
        source='userproject_set',
        many=True,
    )


class ProjectExpandAllSerializer(ProjectSerializer, ProjectLeads):
    """
    Serializes a project with embeded information including
    list of tags, categories and links associated with that project
    as simple strings. It also includes relevant details of every
    user who is a lead and every event associated with this project
    """

    leads = serializers.SerializerMethodField()
    events = EventSerializer(many=True)

    class Meta:
        model = Project
        exclude = ['users']


class ProjectExpandAllWithGithubSerializer(ProjectWithGithubSerializer):
    """
    Serializes a project with embeded information including
    list of tags, categories and links associated with that project
    as simple strings. It also includes relevant details of every
    user and event associated with this project and its github contributor list
    """

    events = EventSerializer(many=True)
    users = UserProjectSerializer(
        source='userproject_set',
        many=True,
    )
