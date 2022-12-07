"""Tests for invoice related methods"""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Request,Invoice,SchoolBankAccount
from lessons.tests.helpers import reverse_with_next

class InvoiceMethodsTestCase(TestCase):

        # Get user to identify request form
    fixtures = [
        'lessons/tests/fixtures/default_user2.json'
    ]


    def setUp(self):
        self.user = User.objects.get(username='michael.kolling@kcl.ac.uk')
        self.request = Request.objects.create(
            # Must be in the form YYYY-MM-DD
            username = self.user,
            availability_date = "2022-12-29",
            availability_time = "08:30",
            instrument = "Violin",
            interval_between_lessons = 5,
            duration_of_lessons = 30
        )

        self.request_2 = Request.objects.create(
            # Must be in the form YYYY-MM-DD
            username = self.user,
            availability_date = "2022-12-29",
            availability_time = "08:30",
            instrument = "Violin",
            interval_between_lessons = 5,
            duration_of_lessons = 30
        )
        #A new invoice was created here because the value of the
        #id of the request changes every time it is generated
        #during testing
        self.invoice = Invoice.objects.create(
            unique_reference_number = "1"+"-"+str(self.request.id),
            invoice_number=str(self.request.id),
            student_id =5,
            paid = False,
            amount = 44,
            currently_paid = 11
            )

        self.school_bank_account = SchoolBankAccount.objects.create(balance = 0.0)

        self.update_url = reverse('update-request', kwargs={'id': self.request.id})


    def test_succesful_invoice_update(self):
        self.client.login(username = self.user.username, password='Password123')
        response = self.client.post(
            self.update_url,
            {
                'username' : self.user,
                'availability_date' : "2023-02-26",
                'availability_time' : "08:30",
                'instrument' : "Double Bass",
                'interval_between_lessons' : 1,
                'duration_of_lessons' : 30
            }
        )
        self.assertEqual(response.status_code, 302)
        self.request.refresh_from_db()
        self.client.get(self.update_url, follow=True)

    def test_unsuccesful_invoice_update(self):
        self.client.login(username = self.user.username, password='Password123')
        self.update_url = reverse('update-request', kwargs={'id': self.request_2.id})
        response = self.client.post(
            self.update_url,
            {
                'username' : self.user,
                'availability_date' : "2023-02-26",
                'availability_time' : "08:30",
                'instrument' : "Double Bass",
                'interval_between_lessons' : 1,
                'duration_of_lessons' : 30
            }
        )
        self.assertEqual(response.status_code, 302)
        self.request.refresh_from_db()
        self.client.get(self.update_url, follow=True)
