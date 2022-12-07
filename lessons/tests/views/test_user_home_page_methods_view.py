"""Tests user (home page) views."""
from django.test import TestCase, Client
from django.urls import reverse
from lessons.models import User, Request, SchoolBankAccount
from lessons.tests.helpers import create_requests, reverse_with_next

class UserMethodsTestCase(TestCase):
    """Tests for the user(home) view."""

    fixtures = [
         'lessons/tests/fixtures/default_user2.json'
    ]
    def setUp(self):
        self.user = User.objects.get(username ="michael.kolling@kcl.ac.uk")

        self.view_bookings_url = reverse("view_bookings")
        self.view_transfers_url = reverse("view_transfers")
        self.view_invoices_url = reverse("view_invoices")
        self.view_balance_and_transactions_url = reverse("balance_and_transactions")

        self.client.login(username=self.user.username, password='Password123')


    def test_view_bookings_url(self):
        self.assertEqual(self.view_bookings_url,"/bookings/")

    def test_view_transfers_url(self):
        self.assertEqual(self.view_transfers_url,"/view_transfers/")

    def test_view_invoices_url(self):
        self.assertEqual(self.view_invoices_url,"/view_invoices/")

    def test_view_balance_and_transactions_url(self):
        self.assertEqual(self.view_balance_and_transactions_url,"/balance_and_transactions/")


    def test_view_bookings(self):
        response = self.client.get(self.view_bookings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings.html')

    def test_view_transfers(self):
        response = self.client.get(self.view_transfers_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_transfers.html')

    def test_view_invoices(self):
        response = self.client.get(self.view_invoices_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_invoices.html')

    def test_view_balance_and_transactions(self):
        response = self.client.get(self.view_balance_and_transactions_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'balance_and_transactions.html')
