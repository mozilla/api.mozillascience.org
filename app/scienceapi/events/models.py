from django.db import models
from datetime import date

from scienceapi.users.models import User
from scienceapi.projects.models import Project


class EventQuerySet(models.query.QuerySet):
    """
    A queryset for Events which allows filtering events
    that occur after the current date(inclusive) and before
    """

    def past(self):
        return self.filter(ends_at__date__lt=date.today())

    def future(self):
        return self.filter(ends_at__date__gte=date.today())

    def slug(self, slug):
        return self.filter(slug=slug)


class Event(models.Model):
    """
    A science event being run, created through the Mozilla
    Science site
    """
    name = models.CharField(max_length=300)
    category = models.CharField(
        max_length=50,
        default='Project Call',
        choices=(
            ('Project Call', 'Project Call'),
            ('Study Group Call', 'Study Group Call'),
            ('Community Call', 'Community Call'),
            ('Workshop', 'Workshop'),
            ('Sprint', 'Sprint'),
            ('MozFest', 'MozFest'),
            ('Conference', 'Conference'),
            ('Meetup', 'Meetup'),
            ('Convening', 'Convening'),
        ),
        help_text='Select the type of event'
    )

    image_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text='URL to an event\'s image.',
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='This appears below the photo in the full-page '
                  'view; should be distinct from the "short description"',
    )
    short_description = models.TextField(
        max_length=300,
        blank=True,
        null=True,
        help_text='This appears below the photo in the card pre-view, '
                  'and below the title in the full-page view',
    )
    slug = models.SlugField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name='Mozilla Science URL Slug',
        help_text='Slug appended to the Mozilla Science event\'s '
                  'url that represents this event',
    )
    is_virtual = models.BooleanField(
        default=False,
        help_text='When selected, events will appear on site converted '
                  'to a visitor\'s local time.',
        verbose_name='Virtual Event'
    )

    timezone = models.CharField(
        max_length=40,
        help_text='Timezone of the place where the event will be held. '
                  'If the event is virtual, use whatever time zone you like '
                  'and enter the times in that zone.'
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
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

    objects = EventQuerySet.as_manager()

    class Meta:
        ordering = ['date_created']

    def __str__(self):
        return str(self.name)
