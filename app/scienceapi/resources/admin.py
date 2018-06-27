from django.contrib import admin

from .models import Resource, Tag


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    ordering = ('name',)


admin.site.register(Tag)
