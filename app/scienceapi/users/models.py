from django.db import models


class User(models.Model):
    """
    A user of the mozilla science site
    """
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    designation = models.CharField(max_length=300)
    email = models.EmailField()
    location = models.CharField(max_length=300)
    biography = models.TextField(blank=True)
    github_id = models.IntegerField(null=True)
    github_username = models.CharField(max_length=200)
    twitter_handle = models.CharField(max_length=200)
    avatar_url = models.URLField(
        max_length=500,
        null=True,
        help_text='URL to user\'s avatar',
    )
    blog = models.URLField(
        max_length=500,
        null=True,
        help_text='URL to user\'s blog',
    )
    company = models.CharField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=200)

    class Meta:
        get_latest_by = 'date_created'

    def __str__(self):
        return str(self.username)
