from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


superusers = [
    {
        'username': 'superuser',
        'password': 'dummy',
        'email': 'superuser@example.com'
    }
]


normalusers = [
    {
        'username': 'user1',
        'password': 'dummy'
    },
    {
        'username': 'user2',
        'password': 'dummy'
    }
]


class Command(BaseCommand):
    help = 'Seed dummy users for testing review apps.'

    def handle(self, *args, **options):
        User = get_user_model()

        for superuser in superusers:
            User.objects.create_superuser(**superuser)

        self.stdout.write(
            self.style.SUCCESS('Successfully created all superusers'))

        for normaluser in normalusers:
            User.objects.create_user(**normaluser)

        self.stdout.write(
            self.style.SUCCESS('Successfully created all normal users'))
