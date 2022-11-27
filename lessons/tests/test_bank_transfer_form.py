"""Unit tests of the bank transfer form."""
from django import forms
from django.test import TestCase
from lessons.forms import InvoiceForm

class InvoiceFormTestCase(TestCase):
    """Unit tests of the request form."""


    def setUp(self):
        self.form_input = {

            "reference_number" : 132,
            "invoice_number" : 43
        }

    def test_valid_sign_up_form(self):
        form = InvoiceForm(data=self.form_input)
        self.assertTrue(form.is_valid())


    #def test_reference_number_must_not_be_blank(self):
    #    self.form_input['reference_number'] = ''
    #    form = InvoiceForm(data=self.form_input)
    #    self.assertFalse(form.is_valid())

    def test_invoice_number_must_not_be_blank(self):
        self.form_input['invoice_number'] = ''
        form = InvoiceForm(data=self.form_input)
        self.assertFalse(form.is_valid())
