from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    raw_id_fields = ('attendees', 'facilitators', 'projects',)
