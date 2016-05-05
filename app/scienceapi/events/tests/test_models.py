import factory
from datetime import datetime
import pytz
from faker import Factory as FakerFactory

from scienceapi.events.models import Event

faker = FakerFactory.create()


class EventFactory(factory.Factory):
    name = factory.LazyAttribute(lambda o: faker.name())
    image_url = factory.LazyAttribute(lambda o: faker.image_url())
    description = factory.LazyAttribute(lambda o: faker.text(max_nb_chars=100))
    slug = factory.LazyAttribute(lambda o: faker.slug())
    starts_at = factory.LazyAttribute(
        lambda o: datetime.utcnow().replace(tzinfo=pytz.utc)
    )
    ends_at = factory.LazyAttribute(
        lambda o: datetime.utcnow().replace(tzinfo=pytz.utc)
    )
    location = factory.LazyAttribute(lambda o: faker.country_code())
    schedule = factory.LazyAttribute(lambda o: faker.text(max_nb_chars=100))
    additional_notes = factory.LazyAttribute(
        lambda o: faker.text(max_nb_chars=100)
    )

    class Meta:
        model = Event
