"""Unit tests for the Request model."""

from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Request
import datetime
from lessons.models import User
class RequestModelTestCase(TestCase):
    # Get user to identify request form
    fixtures = [
        'lessons/tests/fixtures/default_user2.json',
        'lessons/tests/fixtures/terms.json'
    ]

    """Unit tests for the Request model."""
    def setUp(self):
        self.user = User.objects.get(username='michael.kolling@kcl.ac.uk')
        self.request = Request.objects.create(
            # Must be in the form YYYY-MM-DD
            username = self.user,
            availability_date = "2022-12-29",
            availability_time = "08:30",
            instrument = "Violin",
            interval_between_lessons = 1,
            duration_of_lessons = 30
        )

    def test_valid_request(self):
        self._assert_request_is_valid()

    def test_teacher_must_be_not_be_overlong(self):
        self.request.teacher = 'a' * 51
        self._assert_request_is_invalid()

    def test_lesson_dates_in_request(self):
        self.assertIsNotNone(self.request.lesson_dates)
        lesson_dates = []
        for req in Request.objects.all():
            lesson_dates = req.lesson_dates
            self.assertGreater(len(lesson_dates),0 )



    def test_availability_date_can_be_after_one_year(self):
        tod = datetime.datetime.today()
        d = datetime.timedelta(days=365 )
        self.request.availability_date = tod + d
        self._assert_request_is_valid()


    def test_interval_between_lesson_must_be_greater_than_zero(self):
        self.request.interval_between_lessons = -1
        self._assert_request_is_invalid()

    def _assert_request_is_valid(self):
        try:
            self.request.full_clean()
        except(ValidationError):
            self.fail('Test request should be valid')

    def _assert_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.request.full_clean()
