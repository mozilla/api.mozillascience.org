from django.db import models


class StudyGroup(models.Model):
    """
    Study groups on science site
    """
    name = models.CharField(max_length=300)
    link = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text='URL to the study groups\' page',
    )
    location = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        help_text='City and or state name',
    )
    region = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        help_text='Asia, North America, etc.'
    )

    class Meta:
        get_latest_by = 'date_created'

    def __str__(self):
        return str(self.name)
