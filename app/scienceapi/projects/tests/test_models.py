import factory

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
    status = 'Active'
    license = 'MIT'

    class Meta:
        model = Project


class UserFactory(factory.Factory):
    username = factory.LazyAttribute(lambda o: 'John')
    designation = factory.LazyAttribute(
        lambda o: '{a}-designation'.format(a=o.username.lower())
    )
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)
    location = factory.LazyAttribute(
        lambda o: '{a}-location'.format(a=o.username.lower())
    )
    biography = factory.LazyAttribute(
        lambda o: '{a}-biography'.format(a=o.username.lower())
    )
    github_id = factory.Sequence(lambda n: str(n))
    github_username = factory.LazyAttribute(
        lambda o: '{a}-github_username'.format(a=o.username.lower())
    )
    twitter_handle = factory.LazyAttribute(
        lambda o: '{a}-twitter_handle'.format(a=o.username.lower())
    )
    avatar_url = factory.LazyAttribute(
        lambda o: 'http://{a}-avatar_url.com'.format(a=o.username.lower())
    )
    blog = factory.LazyAttribute(
        lambda o: '{a}-blog'.format(a=o.username.lower())
    )
    company = factory.LazyAttribute(
        lambda o: '{a}-company'.format(a=o.username.lower())
    )
    role = factory.LazyAttribute(
        lambda o: '{a}-role'.format(a=o.username.lower())
    )

    class Meta:
        model = User


class UserProjectFactory(factory.Factory):
    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    role = 'Contributor'

    class Meta:
        model = UserProject


class ResourceLinkFactory(factory.Factory):
    url = factory.LazyAttribute(lambda o: 'something.com')
    title = factory.LazyAttribute(lambda o: 'something')
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = ResourceLink
