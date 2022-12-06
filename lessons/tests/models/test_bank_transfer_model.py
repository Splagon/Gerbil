"""Unit tests for the BankTransfer model."""

from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import BankTransfer, User

class BankTransferModelTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='jonathandeer@example.com')
        self.bank_transfer = BankTransfer.objects.create(
        invoice_number= "15945615-7f29-4079-b567-a5a7ac6647a4",
        username =self.user,
        amount = 69.0,
        student_id =1
        )

    def test_valid_bank_transfer(self):
        self.assert_bank_transfer_is_valid()

    def assert_bank_transfer_is_valid(self):
        try:
            self.bank_transfer.full_clean()
        except(ValidationError):
            self.fail('Test Bank Transfer should be valid')

    def assert_bank_transfer_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.bank_transfer.full_clean()
