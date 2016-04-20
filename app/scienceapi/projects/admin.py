from django.contrib import admin

from .models import Project, Category, ResourceLink, Tag

admin.site.register(Project)
admin.site.register(Category)
admin.site.register(ResourceLink)
admin.site.register(Tag)
