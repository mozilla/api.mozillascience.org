from rest_framework import serializers

from scienceapi.utility.github import GithubAPI
from scienceapi.projects.models import (
    Project,
    ResourceLink,
)


class ResourceLinkSerializer(serializers.ModelSerializer):
    """
    Serializes links included in a project by only showing their
    URLS and placeholders
    """
    class Meta:
        model = ResourceLink
        fields = ('url', 'title')


class ProjectWithDetailsSerializer(serializers.ModelSerializer):
    """
    Serializes a list of projects with each project including the
    list of tags, categories and links associated with that project
    as simple strings
    """
    tags = serializers.StringRelatedField(many=True)
    categories = serializers.StringRelatedField(many=True)
    links = ResourceLinkSerializer(many=True)
    github_contributors = GithubAPI
        .get_contributors(github_owner + '/' + github_repository)

    class Meta:
        model = Project
        fields = '__all__'
