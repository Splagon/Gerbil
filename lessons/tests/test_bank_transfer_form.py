"""Unit tests for the bank transfer form."""

from django import forms
from django.test import TestCase
from lessons.forms import BankTransferForm

class BankTransferFormTestCase(TestCase):

    def setUp(self):
        self.form_input = {
        "inv_number":"15945615-7f29-4079-b567-a5a7ac6647a4"
        }

    def test_valid_sign_up_form(self):
        form = BankTransferForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = BankTransferForm()
        self.assertIn('inv_number', form.fields)

    def test_entered_invoice_number_must_not_be_empty(self):
        self.form_input['inv_number'] = ''
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_entered_invoice_number_must_be_in_the_valid_format(self):
        self.form_input['inv_number'] = '15945615-7f29-4079-b567-a5a7ac6647a5'
        form = BankTransferForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    
