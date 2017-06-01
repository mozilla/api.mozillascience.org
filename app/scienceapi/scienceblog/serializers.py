from rest_framework import serializers
from mezzanine.blog.models import BlogPost, BlogCategory
from django.contrib.auth import get_user_model


# Will probably use UserSerializer after users integration
class BlogAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class BlogCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogCategory
        fields = ('id', 'title', 'slug')


class BlogPostSerializer(serializers.ModelSerializer):

    status = serializers.SerializerMethodField()
    author = BlogAuthorSerializer(source='user')
    categories = BlogCategorySerializer(many=True)
    featured_image = serializers.FileField(use_url=True)
    excerpt = serializers.CharField(source='description_from_content')

    class Meta:
        model = BlogPost
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'status',
            'publish_date',
            'excerpt',
            'content',
            'featured_image',
            'author',
            'categories'
        )

    def get_status(self, obj):
        return obj.get_status_display()
