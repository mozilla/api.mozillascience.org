import factory
from faker import Factory as FakerFactory

from scienceapi.resources.models import Resource

faker = FakerFactory.create()


class ResourceFactory(factory.DjangoModelFactory):
    name = factory.LazyAttribute(lambda o: ' '.join(faker.words(nb=4)))
    link = factory.LazyAttribute(lambda o: '{0}.com'.format(o.name.lower()))
    description = factory.LazyAttribute(
        lambda o: 'Long description for {a}'.format(a=o.name.lower())
    )

    class Meta:
        model = Resource
