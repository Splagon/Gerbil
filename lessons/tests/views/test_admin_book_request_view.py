"""Test admin booking view"""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Request
from lessons.tests.helpers import reverse_with_next
from lessons.tests.helpers import LogInTester
import operator
class AdminBookRequestViewTestCase(LogInTester,TestCase ):
    """Test admin booking view"""
 # Get user to identify request form
    fixtures = [
        'lessons/tests/fixtures/default_admin.json'
    ]

    """Unit tests for the Request model."""
    def setUp(self):
        self.user = User.objects.get(username='danielthomas@example.com')
        self.request = Request.objects.create(
            # Must be in the form YYYY-MM-DD
            username = self.user,
            availability_date = "2022-12-29",
            availability_time = "08:30",
            instrument = "Violin",
            interval_between_lessons = 1,
            duration_of_lessons = 30
        )

        self.booking_url = reverse('admin_book_request_form', kwargs={'id': self.request.id, 'requesterId': self.request.requesterId})

    def test_admin_book_request_after_toggle(self):
        self.client.login(username = self.user.username, password='Password123')
        requests_before = len(Request.objects.values())
        response = self.client.post(
            self.booking_url,
            {
                'username' : self.user.username,
                'availability_date' : "2023-02-26",
                'availability_time' : "08:30",
                'instrument' : "Double Bass",
                'interval_between_lessons' : 1,
                'duration_of_lessons' : 30
            }
        )
        self.assertEqual(response.status_code, 302)
        self.request.refresh_from_db()
        self.client.get(self.booking_url, follow=True)
        requests_after = len(Request.objects.values())
        self.assertEquals(requests_before, requests_after)
