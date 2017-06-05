from django.contrib import admin

from .models import StudyGroup


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    ordering = ('location',)
