from django.contrib import admin

import pytz
from .models import Event
from .forms import EventAdminForm


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    raw_id_fields = ('attendees', 'facilitators', 'projects',)

    form = EventAdminForm

    def save_model(self, request, obj, form, change):
        tz = pytz.timezone(obj.timezone)

        # First converting to naive timezone, otherwise localize wont work.
        start = obj.starts_at.replace(tzinfo=None)
        end = obj.ends_at.replace(tzinfo=None)

        # Using the user selected timezone
        obj.starts_at = tz.localize(start)
        obj.ends_at = tz.localize(end)
        super().save_model(request, obj, form, change)

    def get_object(self, request, object_id, from_field):
        obj = super().get_object(request, object_id, from_field)

        if obj is not None:
            tz = pytz.timezone(obj.timezone)

            # Converting the datetimes to user selected timezones
            start = obj.starts_at.astimezone(tz)
            end = obj.ends_at.astimezone(tz)

            # Then converting to naive timezone, otherwise django-templates
            # will change it back to UTC
            obj.starts_at = start.replace(tzinfo=None)
            obj.ends_at = end.replace(tzinfo=None)
        return obj

    class Media:
        css = {
            'all': ('admin/custom-event-admin.css',)
        }
