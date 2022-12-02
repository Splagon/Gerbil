from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import User

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 100

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        user_count = 0
        while user_count < Command.USER_COUNT:
            print(f'Seeding user {user_count}',  end='\r')
            # try:
            self._create_user()
            # except (django.db.utils.IntegrityError):
            #     continue
            user_count += 1
        print('User seeding complete')

    def _create_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        username = self._username(first_name, last_name)
        dateOfBirth = self.faker.date_between('-30y', 'today')
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            dateOfBirth= dateOfBirth,
            password=Command.PASSWORD
        )

    def _username(self, first_name, last_name):
        username = f'{first_name}.{last_name}@example.org'
        return username
