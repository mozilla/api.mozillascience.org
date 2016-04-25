from django.db import models


class Category(models.Model):
    """
    A category of science that a project might be relavant to
    """
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    """
    Tags used to describe properties of a project (such as what
    programming languages does the project use, etc.) and to
    enable filtering projects by these properties
    """
    name = models.CharField(max_length=150)

    def __str__(self):
        return str(self.name)


class Project(models.Model):
    """
    An open-source project on the Mozilla Science website
    """
    name = models.CharField(max_length=300)
    project_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text='URL to the project\'s landing page on the web',
    )
    slug = models.SlugField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name='Mozilla Science URL Slug',
        help_text='Slug appended to the Mozilla Science project\'s '
                  'url that represents this project',
    )
    github_owner = models.CharField(max_length=200)
    github_repository = models.CharField(max_length=300)
    image_url = models.URLField(
        max_length=500,
        null=True,
        blank=True,
        help_text='URL to project\'s image.',
    )
    institution = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        help_text='Institution/Organization this project belongs to',
    )
    description = models.TextField(
        blank=True,
        null=True,
    )
    short_description = models.TextField(
        max_length=300,
        blank=True,
        null=True,
    )
    status = models.BooleanField(
        default=False,
        help_text='Has this project been Approved or not'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    license = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='projects',
        blank=True,
    )
    categories = models.ManyToManyField(
        Category,
        related_name='projects',
        blank=True,
    )

    class Meta:
        get_latest_by = 'date_created'

    def __str__(self):
        return str(self.name)


class ResourceLink(models.Model):
    """
    Links to various resources that are relevant to a project
    """
    url = models.URLField(max_length=500)
    title = models.CharField(max_length=300)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='links'
    )

    def __str__(self):
        return '%s - %s' % (self.title, self.url)
