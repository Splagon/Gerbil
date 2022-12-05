from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django import forms
from lessons.forms import BankTransferForm
from django.urls import reverse
from lessons.models import User
class AddTermViewTestCase(TestCase):
    """Unit tests for the Bank Transfer view."""

    fixtures = [
        'lessons/tests/fixtures/default_user2.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username = "michael.kolling@kcl.ac.uk")
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse("bank_transfer")

    def test_bank_transfer_url(self):
        self.assertEqual(self.url,"/bank_transfer/")

    def test_get_bank_transfer(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bank_transfer.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form,BankTransferForm))
        self.assertFalse(form.is_bound)
