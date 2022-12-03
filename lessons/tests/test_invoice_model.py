"""Unit tests for the Invoice model."""

from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import Invoice

class InvoiceModelTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_invoice.json'
    ]

    def setUp(self):
        self.invoice = Invoice.objects.get(invoice_number="15945615-7f29-4079-b567-a5a7ac6647a4")


    def test_valid_invoice(self):
        self.assert_invoice_is_valid()

    def assert_invoice_is_valid(self):
        try:
            self.invoice.full_clean()
        except(ValidationError):
            self.fail('Test Invoice should be valid')

    def assert_invoice_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.invoice.full_clean()
