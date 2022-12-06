from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import User, Request
from lessons.models import Term
from django.db.utils import IntegrityError
import datetime
from random import randint, random
from .helpers import getDurations, getInstruments,getIntervalBetweenLessons

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 100
    NUMBER_OF_TERMS = 6
    REQUEST_FULFILL_PROBABILITY = 0.75
    # Makes a dictionary for the term dates
    TERM_START_DATES = {
        1 : datetime.datetime(2022, 9, 1),
        2 : datetime.datetime(2022, 10, 31),
        3 : datetime.datetime(2023, 1, 3),
        4 : datetime.datetime(2023, 2, 20),
        5 : datetime.datetime(2023, 4, 17),
        6 : datetime.datetime(2023, 6, 5),
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
        self.create_all_users()
        self.allUsers = User.objects.all()
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
        dateOfBirth = self.faker.date_of_birth(None, 18, 60)
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
            dateOfBirth=self.faker.date_of_birth(None, 18, 60),
            password=Command.PASSWORD
        )

        # request = Request()
        # request.username = User.objects.filter(username="john.doe@example.org")
        # request.availability_time = 

    def create_requests(self):
        request = Request()
        request.username = self.get_random_user()
        request.availability_date = self.get_random_term_date()
        request.interval_between_lessons = randint(1,2)
        #Creates a random int between 0 and length of duration
        randDuration = randint(0, len(getDurations())-1)
        request.duration_of_lessons = getDurations()[randDuration][0]
        #Random int for instrument
        randInstrument = randint(0, len(getInstruments())-1)
        request.instrument = getInstruments()[randInstrument][0]
        request.teacher = self.faker.first_name() + " " + self.faker.last_name()
        request.status = self.get_random_status()
        request.save()
        print("Created request")

    def get_random_user(self):
        index = randint(0,self.allUsers.count()-1)
        return self.allUsers[index]

    def get_random_term_date(self):
        while (True):
            index = randint(1, Command.NUMBER_OF_TERMS)
            termStart = Command.TERM_START_DATES[index]
            today = datetime.datetime.today()
            if (termStart < today):
                return self.faker.date_between(termStart, today)
            print(f'Getting random term data.',  end='\r')
    
    def get_random_status(self):
        if Command.REQUEST_FULFILL_PROBABILITY < random():
            return "test"
        else: 
            return "In Progress"

    def create_petrapickles_admin(self):
        User.objects.create_user(
            username="petra.pickles@example.org",
            first_name="Petra",
            last_name="Pickles",
            dateOfBirth=self.faker.date_of_birth(None, 18, 60),
            password=Command.PASSWORD,
            is_staff = True,
            is_superuser = False
    )

    def create_martymajor_director(self):
        User.objects.create_user(
            username="marty.major@example.org",
            first_name="Marty",
            last_name="Major",
            dateOfBirth=self.faker.date_of_birth(None, 18, 60),
            password=Command.PASSWORD,
            is_staff=True,
            is_superuser=True
            )
