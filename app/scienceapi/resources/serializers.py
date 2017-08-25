from rest_framework import serializers

from scienceapi.resources.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    """
    Serializes a resource with embeded information including
    list of tags associated with that resource
    as simple strings.
    """
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Resource
        fields = '__all__'
