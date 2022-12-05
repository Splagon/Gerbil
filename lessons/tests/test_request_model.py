"""Unit tests for the Request model."""

from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Request
import datetime
from lessons.models import User
class RequestModelTestCase(TestCase):
    # Get user to identify request form
    fixtures = [
        'lessons/tests/fixtures/default_user2.json'
    ]
    
    """Unit tests for the Request model."""
    def setUp(self):
        self.user = User.objects.get(username='michael.kolling@kcl.ac.uk')
        self.request = Request.objects.create(
            # Must be in the form YYYY-MM-DD
            username = self.user,
            availability_date = "2022-12-29",
            availability_time = "08:30",
            instrument = "violin",
            interval_between_lessons = 1,
            # number_of_lessons = 5,
            duration_of_lessons = 30
        )

    def test_valid_request(self):
        self._assert_request_is_valid()

    # def test_time_must_be_after_eight(self):
    #     self.request.availability_time = '03:00'
    #     self._assert_request_is_invalid()

    # def test_time_must_be_before_five_thirty(self):
    #     self.request.availability_time = '17:31'
    #     self._assert_request_is_invalid()

    def test_teacher_must_be_not_be_overlong(self):
        self.request.teacher = 'a' * 51
        self._assert_request_is_invalid()

    # def test_availability_date_must_not_be_before_today(self):
    #     tod = datetime.datetime.today()
    #     d = datetime.timedelta(days=5)

    #     self.request.availability_date = tod - d
    #     self._assert_request_is_invalid()

    # def test_availability_date_must_not_be_after_two_years(self):
    #     tod = datetime.datetime.today()
    #     d = datetime.timedelta(days=365 * 2)
    #     self.request.availability_date = tod + d
    #     self._assert_request_is_invalid()

    def test_availability_date_can_be_after_one_year(self):
        tod = datetime.datetime.today()
        d = datetime.timedelta(days=365 )
        self.request.availability_date = tod + d
        self._assert_request_is_valid()
    

    def test_interval_between_lesson_must_be_greater_than_zero(self):
        self.request.interval_between_lessons = -1
        self._assert_request_is_invalid()


    # def test_interval_between_lessons_must_not_be_blank(self):
    #     self.form_input['interval_between_lessons'] = ''
    #     form = RequestForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())
    
    # def test_duration_of_lessons_must_not_be_blank(self):
    #     self.form_input['duration_of_lessons'] = ''
    #     form = RequestForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())

    # def test_number_of_lessons_must_not_be_blank(self):
    #     self.form_input['number_of_lessons'] = ''
    #     form = RequestForm(data=self.form_input)
    #     self.assertFalse(form.is_valid())

    # def test_instrument_can_be_blank(self):
    #     self.form_input['instrument'] = ()
    #     form = RequestForm(data=self.form_input)
    #     self.assertTrue(form.is_valid())
    
    # def test_teacher_can_be_blank(self):
    #     self.form_input['teacher'] = ()
    #     form = RequestForm(data=self.form_input)
    #     self.assertTrue(form.is_valid())

    def _assert_request_is_valid(self):
        try:
            self.request.full_clean()
        except(ValidationError):
            self.fail('Test request should be valid')

    def _assert_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.request.full_clean()
