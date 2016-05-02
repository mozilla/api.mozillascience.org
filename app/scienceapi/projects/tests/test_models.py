import factory
import datetime

from scienceapi.projects.models import Project, ResourceLink
from scienceapi.users.models import UserProject, User


class ProjectFactory(factory.DjangoModelFactory):
    name = factory.LazyAttribute(lambda o: 'John')
    project_url = factory.LazyAttribute(lambda o: '{a}.com'.format(
        a=o.name.lower()
    ))
    slug = factory.LazyAttribute(lambda o: '{a}-{a}'.format(
        a=o.name.lower()
    ))
    github_owner = factory.LazyAttribute(lambda o: '{a}-github_owner'.format(
        a=o.name.lower()
    ))
    github_repository = factory.LazyAttribute(
        lambda o: '{a}-github_repository'.format(a=o.name.lower())
    )
    image_url = factory.LazyAttribute(
        lambda o: 'http://{a}.com/{a}.png'.format(a=o.name.lower())
    )
    institution = factory.LazyAttribute(
        lambda o: '{a}-institution'.format(a=o.name.lower())
    )
    description = factory.LazyAttribute(
        lambda o: 'Long description for {a}'.format(a=o.name.lower())
    )
    short_description = factory.LazyAttribute(
        lambda o: 'Short description for {a}'.format(a=o.name.lower())
    )
    status = True
    date_created = datetime.date.today()
    date_updated = datetime.date.today()
    license = "MIT"

    class Meta:
        model = Project


class UserFactory(factory.Factory):
    username = 'john'
    name = 'Ali'
    designation = factory.LazyAttribute(lambda o: 'Name!')
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)
    location = factory.LazyAttribute(lambda o: 'Name!')
    biography = factory.LazyAttribute(lambda o: 'Name!')
    github_id = factory.Sequence(lambda n: str(n))
    github_username = factory.LazyAttribute(lambda o: 'Name!')
    twitter_handle = factory.LazyAttribute(lambda o: 'Name!')
    avatar_url = factory.LazyAttribute(lambda o: 'Name!')
    blog = factory.LazyAttribute(lambda o: 'Name!')
    company = factory.LazyAttribute(lambda o: 'Name!')
    date_created = factory.LazyAttribute(lambda o: 'Name!')
    date_updated = factory.LazyAttribute(lambda o: 'Name!')
    role = factory.LazyAttribute(lambda o: 'Name!')

    class Meta:
        model = User


class UserProjectFactory(factory.Factory):
    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    role = 'something'

    class Meta:
        model = UserProject


class ResourceLinkFactory(factory.Factory):
    url = factory.LazyAttribute(lambda o: 'something.com')
    title = factory.LazyAttribute(lambda o: 'something')
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = ResourceLink
