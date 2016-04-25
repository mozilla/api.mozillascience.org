from django.db import models

from scienceapi.projects.models import Project


class User(models.Model):
    """
    A user of the mozilla science site
    """
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    designation = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        null=True,
        blank=True,
    )
    location = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    biography = models.TextField(
        null=True,
        blank=True,
    ),
    github_id = models.IntegerField(null=True)
    github_username = models.CharField(max_length=200)
    twitter_handle = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    avatar_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text='URL to user\'s avatar',
    )
    blog = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text='URL to user\'s blog',
    )
    company = models.CharField(
        max_length=300,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    role = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    projects = models.ManyToManyField(
        Project,
        through='UserProject',
        blank=True,
        related_name='users'
    )

    class Meta:
        get_latest_by = 'date_created'

    def __str__(self):
        return str(self.username)


class UserProject(models.Model):
    """
    A junction model that connects users to projects
    and vice-versa.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=(
            ('LEAD', 'Lead'),
            ('CONTRIBUTOR', 'Contributor')
        ),
        default='CONTRIBUTOR',
    )
