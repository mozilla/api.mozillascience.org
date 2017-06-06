from django.shortcuts import redirect
from rest_framework.generics import ListAPIView, RetrieveAPIView

from mezzanine.blog.models import BlogPost, BlogCategory

from .serializers import BlogPostSerializer, BlogCategorySerializer


def blog_preview(request, *args, **kwargs):
    # Redirect to preview url on frontend. Using a dummy url for now.
    return redirect('https://google.com')


class BlogPostListView(ListAPIView):
    """
    A view that permits a GET to allow listing all blog posts
    in the database

    **Query Parameters** -

    - `?search=` - Search for a blog post

    - `?category=` - Limit blog posts to a particular blog category. A valid
    `category` entry is a pre-existing blog category slug

    - `?year=` - Limit blog posts to a particular year. `year` should be in
    form YYYY eg. `?year=2017`.

    - `?month=` - Given an year limit blog posts to a particular month
    of the year. It is a valid parameters only if `year` is also given.
    eg. `?year=2017&month=11`

    - `?author=` - Given the author username limit blog posts to a particular
    author.
    """
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
    """
    A view that permits a GET to allow listing of a single blog post
    by providing its `id` as a parameter

    """
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        return BlogPost.objects.published(for_user=self.request.user)


class BlogPostSlugView(RetrieveAPIView):
    """
    A view that permits a GET to allow listing of a single blog post
    by providing its `slug` as a parameter

    """
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return BlogPost.objects.filter(slug=self.kwargs['slug'])


class BlogCategoryListView(ListAPIView):
    """
    A view that permits a GET to allow listing of all blog categories

    """

    serializer_class = BlogCategorySerializer
    queryset = BlogCategory.objects.all()
