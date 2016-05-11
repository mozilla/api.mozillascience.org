import factory
import pytz
from faker import Factory as FakerFactory

from scienceapi.events.models import Event

faker = FakerFactory.create()


class EventFactory(factory.Factory):
    name = factory.LazyAttribute(lambda o: faker.name())
    image_url = factory.LazyAttribute(lambda o: faker.image_url())
    description = factory.LazyAttribute(lambda o: faker.text(max_nb_chars=100))
    slug = factory.LazyAttribute(lambda o: faker.slug())
    ends_at = factory.LazyAttribute(
        lambda o: faker.date_time_this_year(
            before_now=False, after_now=True
        ).replace(tzinfo=pytz.utc)
    )
    location = factory.LazyAttribute(lambda o: faker.country_code())
    schedule = factory.LazyAttribute(lambda o: faker.text(max_nb_chars=100))
    additional_notes = factory.LazyAttribute(
        lambda o: faker.text(max_nb_chars=100)
    )

    class Meta:
        model = Event
