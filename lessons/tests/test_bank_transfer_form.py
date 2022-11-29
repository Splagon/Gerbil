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

    
