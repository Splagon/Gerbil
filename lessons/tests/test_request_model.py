"""Unit tests for the Request model."""

from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Request
import datetime
import uuid
class RequestModelTestCase(TestCase):
    """Unit tests for the Request model."""

    def setUp(self):
        self.request = Request.objects.create(
            # Must be in the form YYYY-MM-DD
            id = uuid.uuid4,
            availability_date = "2022-12-29",
            availability_time = "08:30",
            instrument = "violin",
            interval_between_lessons = 5,
            number_of_lessons = 5,
            duration_of_lessons = 30
        )

    def test_valid_request(self):
        self._assert_request_is_valid()


    def _assert_request_is_valid(self):
        try:
            self.request.full_clean()
        except(ValidationError):
            self.fail('Test request should be valid')

    def _assert_request_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.request.full_clean()