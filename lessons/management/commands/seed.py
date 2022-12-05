from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import User, Request, Term
from django.db.utils import IntegrityError

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 100

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_terms()
        self.create_all_users()
        self.allUsers = User.objects.all()

    def create_terms():

    def create_all_users(self):
        user_count = 0

        # creates the predefined users
        try:
            self.create_johndoe_student()
            self.create_petrapickles_admin()
            self.create_martymajor_director()
        except (IntegrityError):
            pass

        # creates all the random users
        while user_count < Command.USER_COUNT:
            print(f'Seeding user {user_count}',  end='\r')
            try:
                self.create_user()
            except (IntegrityError):
                continue
            user_count += 1
        print('User seeding complete')

    def create_user(self):
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

    def create_johndoe_student(self):
        User.objects.create_user(
            username="john.doe@example.org",
            first_name="John",
            last_name="Doe",
            dateOfBirth=self.faker.date_between('-50y', 'today'),
            password=Command.PASSWORD
        )

        request = Request()
        request.username = User.objects.filter(username="john.doe@example.org")
        request.availability_time = 



    def create_petrapickles_admin(self):
        User.objects.create_user(
            username="petra.pickles@example.org",
            first_name="Petra",
            last_name="Pickles",
            dateOfBirth=self.faker.date_between('-30y', 'today'),
            password=Command.PASSWORD,
            is_staff = True,
            is_superuser = False
    )

    def create_martymajor_director(self):
        User.objects.create_user(
            username="marty.major@example.org",
            first_name="Marty",
            last_name="Major",
            dateOfBirth=self.faker.date_between('-30y', 'today'),
            password=Command.PASSWORD,
            is_staff=True,
            is_superuser=True
            )
