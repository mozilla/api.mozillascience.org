from django.contrib import admin

from .models import Project, Category, ResourceLink, Tag


class CategoryInline(admin.TabularInline):
    model = Project.categories.through


class TagInline(admin.TabularInline):
    model = Project.tags.through


class ResourceLinkInline(admin.TabularInline):
    model = ResourceLink
    verbose_name = 'Link'


class UserInline(admin.TabularInline):
    model = Project.users.through
    verbose_name = 'User'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [
        CategoryInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [
        TagInline,
    ]
    ordering = ['name']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ResourceLinkInline,
        UserInline,
    ]
    search_fields = ('name',)


admin.site.register(ResourceLink)
