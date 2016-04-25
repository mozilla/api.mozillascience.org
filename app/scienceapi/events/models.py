from django.db import models

from scienceapi.users.models import User
from scienceapi.projects.models import Project


class Event(models.Model):
    """
    A science event being run, created through the Mozilla
    Science site
    """
    name = models.CharField(max_length=300)
    image_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text='URL to an event\'s image.',
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    slug = models.SlugField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name='Mozilla Science URL Slug',
        help_text='Slug appended to the Mozilla Science event\'s '
                  'url that represents this event',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    timezone = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    location = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    schedule = models.TextField(
        blank=True,
        null=True,
    )
    additional_notes = models.TextField(
        blank=True,
        null=True,
    )
    created_by = models.ForeignKey(
        User,
        related_name='events_created'
    )
    attendees = models.ManyToManyField(
        User,
        related_name='events_attended',
        blank=True,
    )
    facilitators = models.ManyToManyField(
        User,
        related_name='events_facilitated',
        blank=True,
    )
    projects = models.ManyToManyField(
        Project,
        related_name='events',
        blank=True,
    )

    class Meta:
        get_latest_by = 'date_created'

    def __str__(self):
        return str(self.name)
