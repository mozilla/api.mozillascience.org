import factory
from faker import Factory as FakerFactory

from scienceapi.projects.models import Project, ResourceLink
from scienceapi.users.models import UserProject
from scienceapi.users.tests.test_models import UserFactory


faker = FakerFactory.create()


class ProjectFactory(factory.DjangoModelFactory):
    name = factory.LazyAttribute(lambda o: ' '.join(faker.words(nb=4)))
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

    @factory.post_generation
    def events(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for event in extracted:
                self.events.add(event)

    class Meta:
        model = Project


class UserProjectFactory(factory.Factory):
    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    role = 'Contributor'

    class Meta:
        model = UserProject


class ResourceLinkFactory(factory.Factory):
    url = factory.LazyAttribute(lambda o: faker.url())
    title = factory.LazyAttribute(lambda o: ' '.join(faker.words(nb=4)))
    project = factory.SubFactory(ProjectFactory)

    class Meta:
        model = ResourceLink
