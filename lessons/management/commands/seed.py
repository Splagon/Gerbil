from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import Adult, User, Request, AdultChildRelationship
from lessons.models import Term
from django.db.utils import IntegrityError
import datetime
from random import randint, random
from lessons.helpers import getDurations, getInstruments


class Command(BaseCommand):
    PASSWORD = "Password123"
    ADULT_USER_COUNT = 100
    CHILDREN_USER_COUNT = 100
    REQUEST_COUNT = 100
    JOHNDOE_REQUEST_COUNT = 5
    NUMBER_OF_TERMS = 6
    REQUEST_FULFILL_PROBABILITY = 0.75
    # Makes a dictionary for the term dates
    TERM_START_DATES = {
        1: datetime.datetime(2022, 9, 1),
        2: datetime.datetime(2022, 10, 31),
        3: datetime.datetime(2023, 1, 3),
        4: datetime.datetime(2023, 2, 20),
        5: datetime.datetime(2023, 4, 17),
        6: datetime.datetime(2023, 6, 5),
    }
    TERM_END_DATES = {
        1: datetime.datetime(2022, 10, 21),
        2: datetime.datetime(2022, 12, 16),
        3: datetime.datetime(2023, 2, 10),
        4: datetime.datetime(2023, 3, 31),
        5: datetime.datetime(2023, 5, 26),
        6: datetime.datetime(2023, 7, 21),
    }

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_terms()
        self.create_all_adult_users()
        self.allAdultUsers = User.objects.filter(is_adult=True)
        self.create_all_children_users()
        self.allChildUsers = User.objects.filter(is_adult = False)
        self.create_requests()

    def create_terms(self):
        """Uses the dictionaries to add data for the term dates"""
        startDates = Command.TERM_START_DATES
        endDates = Command.TERM_END_DATES
        for i in range(Command.NUMBER_OF_TERMS):
            term = Term()
            term.termName = f'Term {i+1}'
            term.startDate = startDates[i+1]
            term.endDate = endDates[i+1]
            term.save()
            print(f'Seeding term {i+1}',  end='\r')
        print('Term seeding complete')

    def create_all_adult_users(self):
        self.create_predefined_users()
        self.create_all_adult_users()

    def create_predefined_users(self):
        # creates the predefined users
        try:
            self.create_adult_users("john.doe@example.org", "John", "Doe", False, False)
            self.create_adult_users("petra.pickles@example.org", "Petra", "Pickles", True, False)
            self.create_adult_users("marty.major@example.org", "Marty", "Major", True, True)
        except (IntegrityError):
            pass

    def create_all_adult_users(self):
        user_count = 0
        # creates all the random users
        while user_count < Command.ADULT_USER_COUNT:
            print(f'Seeding user {user_count}',  end='\r')
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            username = self._username(first_name, last_name)
            try:
                self.create_adult_users(username, first_name, last_name, False, False)
            except (IntegrityError):
                continue
            user_count += 1
        print('User seeding complete')

    def create_adult_users(self, username, first_name, last_name, isAdmin, isDirector):
        dateOfBirth = self.faker.date_of_birth(None, 18, 60)
        Adult.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            dateOfBirth=dateOfBirth,
            password=Command.PASSWORD,
            is_staff=isAdmin,
            is_superuser=isDirector
        )

    def create_all_children_users(self):
        self.create_predefined_children()
        self.create_random_children()
        
    def create_predefined_children(self):
        try:
            self.create_children_user(
                "alice.doe@example.org", "Alice", "Doe", "john.doe@example.org")
            self.create_children_user(
                "bob.doe@example.org", "Bob", "Doe", "john.doe@example.org")
        except (IntegrityError):
            pass

    def create_random_children(self):
        user_count = 0
        # creates all the random users
        while user_count < Command.CHILDREN_USER_COUNT:
            print(f'Seeding children {user_count}',  end='\r')
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            username = self._username(first_name, last_name)
            parent_username = self.get_random_adult_user()
            try:
                self.create_children_user(username, first_name, last_name, parent_username)
            except (IntegrityError):
                continue
            user_count += 1
        print('Children user seeding complete')

    def create_children_user(self, username, first_name, last_name, parent_username):
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            # Has to be under 18 as they are a child
            dateOfBirth=self.faker.date_of_birth(None, 5, 18),
            password=Command.PASSWORD,
            is_adult=False
        )
        # Creates the corresponding parent realtionship for the child
        relationship = AdultChildRelationship()
        relationship.adult = Adult.objects.get(username=parent_username)
        relationship.child = User.objects.get(username=username)
        relationship.save()

    def _username(self, first_name, last_name):
        username = f'{first_name}.{last_name}@example.org'
        return username

    def create_requests(self):
        # makes requests for John Doe
        john_doe = User.objects.get(username="john.doe@example.org")
        for i in range(Command.JOHNDOE_REQUEST_COUNT):
            self.create_a_request(john_doe)
        # Makes the requests for other users
        request_count = 0
        while request_count < Command.REQUEST_COUNT:
            print(f'Seeding request {request_count}',  end='\r')
            self.create_a_request(self.get_random_adult_user())
            request_count += 1
        print("Request seeding complete")

    def choose_which_user_request(self):
        pass

    def create_a_request(self, user):
        request = Request()
        request.username = user
        request.availability_date = self.get_random_term_date()
        request.interval_between_lessons = randint(1, 2)
        # Creates a random int between 0 and length of duration
        randDuration = randint(0, len(getDurations())-1)
        request.duration_of_lessons = getDurations()[randDuration][0]
        # Random int for instrument
        randInstrument = randint(0, len(getInstruments())-1)
        request.instrument = getInstruments()[randInstrument][0]
        request.teacher = self.faker.first_name() + " " + self.faker.last_name()
        request.status = self.get_random_status()
        request.save()

    # def get_user(self, username):
    #     for user in self.allAdultUsers:
    #         if user.username == username:
    #             return user

    def get_random_adult_user(self):
        index = randint(0, self.allAdultUsers.count()-1)
        return self.allAdultUsers[index]

    def get_random_term_date(self):
        while (True):
            index = randint(1, Command.NUMBER_OF_TERMS)
            termStart = Command.TERM_START_DATES[index]
            today = datetime.datetime.today()
            if (termStart < today):
                return self.faker.date_between(termStart, today)
            print(f'Getting random term data.',  end='\r')

    def get_random_status(self):
        return "Booked" if Command.REQUEST_FULFILL_PROBABILITY > random() else "In Progress"
