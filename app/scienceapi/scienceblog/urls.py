from django.conf.urls import url, include

from .views import (
    blog_preview,
    BlogPostView,
    BlogPostListView,
    BlogPostSlugView,
    BlogCategoryListView
)


blog_post_patterns = [
    url(r'^$',
        BlogPostListView.as_view(),
        name='blog-post-list'),

    url(r'^(?P<pk>[0-9]+)/',
        BlogPostView.as_view(),
        name='blog-post'),

    url(r'^(?P<slug>[-\w]+)/',
        BlogPostSlugView.as_view(),
        name='blog-post-slug'),
]

urlpatterns = [
    url(r'^posts/',
        include(blog_post_patterns)),

    url(r'^categories/',
        BlogCategoryListView.as_view(),
        name='blog-category-list'),

    # Mezzanine send users to `blog_post_detail` route for previewing blogs.
    url(r'^preview/(?P<slug>.+)$',
        blog_preview,
        name='blog_post_detail'),
]
