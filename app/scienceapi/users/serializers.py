from rest_framework import serializers

from scienceapi.users.models import User
from scienceapi.projects.models import Project


class ProjectWithoutDetailsSerializer(serializers.ModelSerializer):
    """
    Serializes a list of projects without additional information
    such as links and github_contributors. Useful for including the project
    relationship in other serializers.
    """
    tags = serializers.StringRelatedField(many=True)
    categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = Project
        fields = '__all__'


class UserWithDetailsSerializer(serializers.ModelSerializer):
    """
    Serializes a list of users with data including the list of projects
    that the user created.
    """
    projects = ProjectWithoutDetailsSerializer(many=True)

    class Meta:
        model = User
        fields = '__all__'
