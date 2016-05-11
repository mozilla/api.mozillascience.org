import factory
from faker import Factory as FakerFactory

from scienceapi.study_groups.models import StudyGroup

faker = FakerFactory.create()


class StudyGroupFactory(factory.DjangoModelFactory):
    name = factory.LazyAttribute(lambda o: ' '.join(faker.words(nb=4)))
    link = factory.LazyAttribute(lambda o: '{a}.com'.format(
        a=o.name.lower()
    ))
    location = factory.LazyAttribute(lambda o: ' '.join(faker.words(nb=4)))
    region = factory.LazyAttribute(lambda o: ' '.join(faker.words(nb=4)))

    class Meta:
        model = StudyGroup
