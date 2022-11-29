"""Unit tests of the bank transfer form."""
from django import forms
from django.test import TestCase
from lessons.forms import InvoiceForm

class InvoiceFormTestCase(TestCase):
    """Unit tests of the request form."""


    def setUp(self):
        self.form_input = {
            "password": "12-345"
        }

    def test_invalid_invoice_form(self):
        self.form_input['password'] = 'a'
        form = InvoiceForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invoice_number_must_not_be_blank(self):
       self.form_input['password'] = ''
       form = InvoiceForm(data=self.form_input)
       self.assertFalse(form.is_valid())

    def test_invoice_must_contain_dash(self):
        self.form_input['password'] = '123'
        form = InvoiceForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invoice_must_contain_reference_model(self):
        self.form_input['password'] = '-123'
        form = InvoiceForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invoice_number_cannot_contain__more_than_one_dash(self):
        self.form_input['password'] = '1--123'
        form = InvoiceForm(data=self.form_input)
        self.assertFalse(form.is_valid())
