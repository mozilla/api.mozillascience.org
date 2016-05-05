import factory
from faker import Factory as FakerFactory

from scienceapi.users.models import User

faker = FakerFactory.create()


class UserFactory(factory.Factory):
    name = factory.LazyAttribute(lambda o: faker.name())
    username = factory.LazyAttribute(lambda o: faker.user_name())
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
