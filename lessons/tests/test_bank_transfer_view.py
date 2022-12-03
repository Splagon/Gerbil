"""Unit tests of the bank transfer view."""
from django.test import TestCase
from django import forms
from lessons.forms import BankTransferForm
from django.urls import reverse
from ..models import User


class InvoiceViewTestCase(TestCase):
    pass

    #def setUp(self):
        #self.url = reverse("bank_transfer")


    #def test_sign_up_url(self):
        #self.assertEqual(self.url,"/bank_transfer/")
