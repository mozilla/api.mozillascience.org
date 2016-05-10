from django.db import models


class StudyGroup(models.Model):
    """
    Study groups on science site
    """
    name = models.CharField(max_length=300)
    link = models.URLField(
        max_length=500,
        help_text='URL to the study groups\' page',
    )
    location = models.CharField(
        max_length=300,
        help_text='City and or state name',
    )
    region = models.CharField(
        max_length=300,
        help_text='Asia, North America, etc.'
    )

    def __str__(self):
        return str('{name}, {location}, {region}'.format(
            name=self.name, location=self.location, region=self.region
        ))
