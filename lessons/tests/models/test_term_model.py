from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Term
import datetime

class TermModelTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/terms.json']

    def setUp(self):
        self.term = Term.objects.get(pk = 1)

    def test_valid_term(self):
        self._assert_term_is_valid()

    #start date
    def test_start_date_cannot_be_blank(self):
        self.term.startDate = None
        self._assert_term_is_invalid()

    def test_start_date_must_be_be_unique(self):
        second_term = self._create_second_term()
        self.term.startDate = second_term.startDate
        self._assert_term_is_invalid()

    #end date
    def test_end_date_cannot_be_blank(self):
        self.term.endDate = None
        self._assert_term_is_invalid()

    def test_end_date_must_be_unique(self):
        second_term = self._create_second_term()
        self.term.endDate = second_term.endDate
        self._assert_term_is_invalid()

    #user validation

    def _assert_term_is_valid(self):
        try:
            self.term.full_clean()
        except (ValidationError):
            self.fail('Test term should be valid.')

    def _assert_term_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.term.full_clean()

    def _create_second_term(self):
        term = Term.objects.get(pk=2)
        return term
