from django.db import models


class Tag(models.Model):
    """
    Tags used to describe properties of a resources
    """
    name = models.CharField(max_length=150)

    def __str__(self):
        return str(self.name)


class Resource(models.Model):
    """
    Resource on the Mozilla Science resource's page
    """
    name = models.CharField(max_length=300)
    link = models.URLField(
        max_length=500,
        help_text='URL to the resource\'s landing page on the web',
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='resources',
        blank=True,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)
