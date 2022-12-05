"""Unit tests for the SchoolBankAccount model."""
from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import SchoolBankAccount

class SchoolBankAccountModelTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_school_bank_account.json'
    ]

    def setUp(self):
        self.school_bank_account = SchoolBankAccount.objects.get(pk=1)


    def test_valid_school_bank_account(self):
        self.assert_school_bank_account_is_valid()

    def assert_school_bank_account_is_valid(self):
        try:
            self.school_bank_account.full_clean()
        except(ValidationError):
            self.fail('Test SchoolBankAccount should be valid')

    def assert_school_bank_account_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.school_bank_account.full_clean()
