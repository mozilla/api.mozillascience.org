import pytz
from faker import Factory as FakerFactory

from scienceapi.users.tests.test_models import UserFactory
from scienceapi.events.tests.test_models import EventFactory
from scienceapi.projects.tests.test_models import (
    ProjectFactory,
    UserProjectFactory,
)

faker = FakerFactory.create()


def create_user_project(user, project):
    UserProjectFactory.build(
        project=project,
        user=user,
        role='Lead',
    ).save()


def create_projects():
    projects = [ProjectFactory() for i in range(3)]
    for project in projects:
        project.save()
    return projects


def create_user():
    user = UserFactory()
    user.save()
    return user


def create_events():
    events = ({
        'past': EventFactory(
            starts_at=faker.date_time_this_year(
                before_now=True, after_now=False
            ).replace(tzinfo=pytz.utc)),
        'future': EventFactory(
            starts_at=faker.date_time_this_year(
                before_now=False, after_now=True
            ).replace(tzinfo=pytz.utc)),
    })
    events['past'].save()
    events['future'].save()
    return events


def create_project_event(project, event):
    project.events.add(event)
    project.save()


def add_attendees(user, event):
    event.attendees.add(user)
    event.save()


def add_facilitators(user, event):
    event.facilitators.add(user)
    event.save()
