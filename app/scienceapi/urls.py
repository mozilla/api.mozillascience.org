"""scienceapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from mezzanine.conf import settings


adminpatterns = [
    url(r'^password_reset/$', auth_views.password_reset,
        name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^', include(admin.site.urls)),
]

apipatterns = [
    url(r'^projects/', include('scienceapi.projects.urls')),
    url(r'^users/', include('scienceapi.users.urls')),
    url(r'^events/', include('scienceapi.events.urls')),
    url(r'^study-groups/', include('scienceapi.study_groups.urls')),
    url(r'^resources/', include('scienceapi.resources.urls')),
    url(r'^blog/', include('scienceapi.scienceblog.urls')),
]

authpatterns = [
    url(r'^logout/', auth_views.logout,
        {'next_page': settings.LOGOUT_REDIRECT_URL}),
    url(r'^', include('social_django.urls'))
]

urlpatterns = [
    url(r'^admin/', include(adminpatterns)),
    url(r'^api/', include(apipatterns)),
    url(r'^auth/', include(authpatterns)),
    url(r'^', include(apipatterns))
]


if settings.USE_S3 is not True:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
