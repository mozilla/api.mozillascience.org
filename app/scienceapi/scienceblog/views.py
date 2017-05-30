from django.shortcuts import redirect
from rest_framework.generics import ListAPIView, RetrieveAPIView

from mezzanine.blog.models import BlogPost, BlogCategory

from .serializers import BlogPostSerializer, BlogCategorySerializer


def blog_preview(request, *args, **kwargs):
    # Redirect to preview url on frontend. Using a dummy url for now.
    return redirect('https://google.com')


class BlogPostListView(ListAPIView):

    serializer_class = BlogPostSerializer

    def get_queryset(self):
        category = self.request.GET.get('category', None)
        search = self.request.GET.get('search', None)
        year = self.request.GET.get('year', None)
        month = self.request.GET.get('month', None)
        author = self.request.GET.get('author', None)

        blog_posts = BlogPost.objects.published(for_user=self.request.user)

        if year is not None:
            blog_posts = blog_posts.filter(publish_date__year=year)
            if month is not None:
                blog_posts = blog_posts.filter(publish_date__month=month)

        if category is not None:
            blog_posts = blog_posts.filter(categories__slug=category)

        if author is not None:
            blog_posts = blog_posts.filter(user__username=author)

        if search is not None:
            blog_posts = blog_posts.search(search)

        return blog_posts


class BlogPostView(RetrieveAPIView):

    serializer_class = BlogPostSerializer

    def get_queryset(self):
        return BlogPost.objects.published(for_user=self.request.user)


class BlogPostSlugView(RetrieveAPIView):

    serializer_class = BlogPostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return BlogPost.objects.filter(slug=self.kwargs['slug'])


class BlogCategoryListView(ListAPIView):

    serializer_class = BlogCategorySerializer
    queryset = BlogCategory.objects.all()
