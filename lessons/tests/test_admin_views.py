"""Tests admin views."""
from django.test import TestCase, Client
from django.urls import reverse
from lessons.models import User, Request, SchoolBankAccount
from lessons.tests.helpers import create_requests, reverse_with_next

class RequestViewTestCase(TestCase):
    """Tests of the request view."""

    fixtures = [
        'lessons/tests/fixtures/default_admin.json',
         'lessons/tests/fixtures/default_user2.json'

    ]
    def setUp(self):
        #Standard user
        self.user_2 = User.objects.get(username ="michael.kolling@kcl.ac.uk")
        #Admin
        self.user = User.objects.get(username = "danielthomas@example.com")
        self.client.login(username=self.user.username, password="Password123")
        self.admin_view_school_balance_and_incoming_transfers_url = reverse("admin_view_school_balance_and_transfers")
        self.admin_view_bookings_url= reverse("admin_view_bookings")
        self.admin_check_student_balance_and_transactions_url = reverse("admin_check_student_balance_and_transactions")
        # self.admin_view_user_invoices_url = reverse("admin_view_user_invoice")
        # self.admin_view_user_transfers_url = reverse("admin_view_user_transfers")
        self.admin_view_user_invoices_url = reverse("admin_view_user_invoice", args=[self.user_2.id])
        self.admin_view_user_transfers_url = reverse("admin_view_user_transfers", args=[self.user_2.id])

        self.school_bank_account = SchoolBankAccount.objects.create(
        id = 1,
        balance = 0.0)


    def test_admin_view_school_balance_and_incoming_transfers_url(self):
        self.assertEqual(self.admin_view_school_balance_and_incoming_transfers_url,"/admin/view_school_balance_and_transfers/")

    def test_admin_view_bookings_url(self):
        self.assertEqual(self.admin_view_bookings_url,"/admin/view_bookings/")

    def test_admin_check_student_balance_and_transactions_url(self):
        self.assertEqual(self.admin_check_student_balance_and_transactions_url,"/admin/check_student_balance_and_transactions/")

    def test_admin_view_user_invoices_url(self):
        self.assertEqual(self.admin_view_user_invoices_url,"/admin/view_user_invoice/" + str(self.user_2.id))

    def test_admin_view_user_transfers_url(self):
        self.assertEqual(self.admin_view_user_transfers_url,"/admin/view_user_transfers/" + str(self.user_2.id))



    def test_admin_get_school_bank_account_and_incoming_transfers_url(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.admin_view_school_balance_and_incoming_transfers_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/admin_view_school_balance_and_transfers.html')

    def test_admin_get_view_bookings(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.admin_view_bookings_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/admin_bookings.html')

    def test_admin_check_student_balance_and_transactions(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.admin_check_student_balance_and_transactions_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/admin_check_student_balance_and_transactions.html')

    def test_admin_view_user_invoices(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.admin_view_user_invoices_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"view_invoices.html")

    def test_admin_view_user_transfers(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.admin_view_user_transfers_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,"view_transfers.html")
