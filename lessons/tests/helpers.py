from django.urls import reverse
from lessons.models import Request
import datetime
class LogInTester:
    def _is_logged_in(self):
        return "_auth_user_id" in self.client.session.keys()


def create_requests(user, from_count, to_count):
    "Create unique requests for testing purposes"
    for count in range(from_count, to_count):
        username = user
        availability_date = datetime.date(year=2023, month=1, day=1)
        availability_time = datetime.time(hour=8, minute=30)
        duration_of_lessons = 5
        interval_between_lessons = 5
        number_of_lessons = 5
        instrument= 'violin'
        teacher = f'Request__{count}'
        #number_of_lessons=number_of_lessons,
        request = Request(username=username, availability_date=availability_date, availability_time=availability_time, duration_of_lessons=duration_of_lessons, interval_between_lessons=interval_between_lessons, teacher=teacher, instrument=instrument)
        request.save()

def reverse_with_next(url_name, next_url):
    url = reverse(url_name)
    url += f"?next={next_url}"
    return url
