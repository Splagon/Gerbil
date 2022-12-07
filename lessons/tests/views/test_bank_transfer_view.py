from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django import forms
from lessons.forms import BankTransferForm
from django.urls import reverse
from lessons.models import User,Invoice,Request,SchoolBankAccount
import uuid
class BankTransferViewTestCase(TestCase):

    """Unit tests for the Bank Transfer view."""

    fixtures = [
        'lessons/tests/fixtures/default_user2.json',
        'lessons/tests/fixtures/default_invoice.json',
        'lessons/tests/fixtures/default_invoice2.json',
        'lessons/tests/fixtures/default_invoice3.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='michael.kolling@kcl.ac.uk')
        self.url = reverse('bank_transfer')
        self.form_input = {
        "inv_number":"15945615-7f29-4079-b567-a5a7ac6647a4",
        "paid_amount": 43.00
        }
        self.invoice = Invoice.objects.get(invoice_number="15945615-7f29-4079-b567-a5a7ac6647a4")
        self.invoice2 = Invoice.objects.get(invoice_number="15945615-7f29-4079-b00b-b5a7ac6647a3")

        self.request = Request.objects.create(
            # Must be in the form YYYY-MM-DD
            id = uuid.UUID(self.form_input["inv_number"]),
            username = self.user,
            availability_date = "2022-12-29",
            availability_time = "08:30",
            instrument = "violin",
            interval_between_lessons = 5,
            # number_of_lessons = 5,
            duration_of_lessons = 30
        )
        self.request_2=Request.objects.create(
        id = uuid.UUID("15945615-7f29-4079-b00b-b5a7ac6647a3"),
        username = self.user,
        availability_date = "2022-12-29",
        availability_time = "08:30",
        instrument = "violin",
        interval_between_lessons = 5,
        # number_of_lessons = 5,
        duration_of_lessons = 45
        )
        self.request_3=Request.objects.create(
        id = uuid.UUID("25945612-8f29-4069-b00b-b2a7ac6647a8"),
        username = self.user,
        availability_date = "2022-12-29",
        availability_time = "08:30",
        instrument = "violin",
        interval_between_lessons = 5,
        # number_of_lessons = 5,
         duration_of_lessons = 45
         )

        self.school_bank_account = SchoolBankAccount.objects.create(
         id = 1,
         balance = 0.0)

    def test_bank_transfer_url(self):
        self.assertEqual(self.url,"/bank_transfer/")

    def test_get_request_bank_transfer(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'bank_transfer.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BankTransferForm))

    def test_unsuccessful_bank_transfer_invoice_doesnt_exist(self):
        self.form_input["inv_number"] = "15945615-7f29-4079-b567-a5a7ac6647bc"
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank_transfer.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BankTransferForm))

    def test_unsuccessful_bank_transfer_incorrect_amount(self):

        self.form_input["paid_amount"] = "abc"
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank_transfer.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BankTransferForm))


    def test_successful_bank_transfer_over_pay(self):
        self.form_input["paid_amount"] = 500
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank_transfer.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BankTransferForm))

    def test_successful_bank_transfer_exact_amount(self):
         self.form_input["paid_amount"] = 100
         self.client.login(username=self.user.username, password='Password123')
         response = self.client.post(self.url, self.form_input, follow=True)
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response, 'bank_transfer.html')
         form = response.context['form']
         self.assertTrue(isinstance(form, BankTransferForm))

    def test_successful_bank_transfer_less_than_amount(self):
         self.form_input["paid_amount"] = 23
         self.invoice.currently_paid = 100
         self.client.login(username=self.user.username, password='Password123')
         response = self.client.post(self.url, self.form_input, follow=True)
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response, 'bank_transfer.html')
         form = response.context['form']
         self.assertTrue(isinstance(form, BankTransferForm))

    def test_successful_bank_transfer_less_than_amount_not_enough(self):
         self.form_input["paid_amount"] = 4
         self.invoice.currently_paid = 100
         self.client.login(username=self.user.username, password='Password123')
         response = self.client.post(self.url, self.form_input, follow=True)
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response, 'bank_transfer.html')
         form = response.context['form']
         self.assertTrue(isinstance(form, BankTransferForm))

    def test_successful_bank_transfer_invoice_has_been_already_paid(self):
         self.form_input["inv_number"] = "15945615-7f29-4079-b00b-b5a7ac6647a3"
         self.invoice.paid=True
         self.client.login(username=self.user.username, password='Password123')
         response = self.client.post(self.url, self.form_input, follow=True)
         self.assertEqual(response.status_code, 200)
         self.assertTemplateUsed(response, 'bank_transfer.html')
         form = response.context['form']
         self.assertTrue(isinstance(form, BankTransferForm))


    def test_request_does_not_exist(self):
        self.form_input["inv_number"] = "25945612-8f29-4069-b00b-b2a7ac6647a2"
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bank_transfer.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, BankTransferForm))
