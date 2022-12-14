"""Test admin request methods"""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Request,SchoolBankAccount,Invoice
from lessons.tests.helpers import reverse_with_next
from lessons.tests.helpers import LogInTester
import operator
class AdminRequestMethodsTestCase(LogInTester,TestCase ):
    """Unit tests for the Request model."""
    fixtures = [
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='danielthomas@example.com')
        self.request = Request.objects.create(
            # Must be in the form YYYY-MM-DD
            username = self.user,
            availability_date = "2022-12-29",
            availability_time = "08:30",
            instrument = "Violin",
            interval_between_lessons = 1,
            # number_of_lessons = 5,
            duration_of_lessons = 30
        )

        self.invoice = Invoice.objects.create(
            unique_reference_number = "1"+"-"+str(self.request.id),
            invoice_number=str(self.request.id),
            student_id =5,
            paid = False,
            amount = 44,
            currently_paid = 11

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
        # Initialise a school bank account to allow users to make transfers
        self.school_bank_account = SchoolBankAccount.objects.create(balance = 0.0)

        self.delete_url = reverse('admin_delete_requests', kwargs={'id': self.request.id})
        self.update_url = reverse('admin_update_requests', kwargs={'id': self.request.id})
        self.view_requests_url = reverse('admin_view_requests')

    def test_admin_delete_request_url(self):
        self.assertEqual(self.delete_url,f'/admin/delete_request/{self.request.id}')

    def test_admin_view_request_url(self):
        self.assertEqual(self.view_requests_url, f'/admin/view_requests/')
        self.client.get(self.view_requests_url, follow=True)

    def test_admin_login_required(self):
        response = self.client.get(self.view_requests_url)
        self.assertRedirects(response, reverse('admin_log_in')+'?next=/admin/'+'view_requests/')

    def test_admin_get_view_requests(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.view_requests_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/admin_view_requests.html')

    def test_admin_update_request_url(self):
        self.assertEqual(self.update_url,f'/admin/update_request/{self.request.id}')

    def test_admin_is_user_staff_type(self):
        self.assertTrue(self.user, operator.attrgetter('is_staff'))

    # Check that the database gets updated once a request is deleted
    def test_admin_delete_request_after_toggle(self):
        self.client.login(username = self.user.username, password='Password123')
        self.assertTrue(self._is_logged_in())
        requests_before = len(Request.objects.values())
        self.client.get(self.delete_url, follow=True)
        requests_after = len(Request.objects.values())
        self.assertEquals(requests_before, requests_after+1)

    # Check that the database gets updated once a request is updated
    def test_admin_update_request_after_toggle(self):
        self.client.login(username = self.user.username, password='Password123')
        requests_before = len(Request.objects.values())
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
        requests_after = len(Request.objects.values())
        self.assertEquals(requests_before, requests_after)

    def test_unsuccesful_admin_invoice_update(self):
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
