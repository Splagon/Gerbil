"""Test delete request method"""
from django.test import TestCase
from django.urls import reverse
from lessons.models import User, Request
from lessons.tests.helpers import reverse_with_next

class RequestMethodsTestCase(TestCase):

        # Get user to identify request form
    fixtures = [
        'lessons/tests/fixtures/default_user2.json'
    ]
    
    """Unit tests for the Request model."""
    def setUp(self):
        self.user = User.objects.get(username='michael.kolling@kcl.ac.uk')
        self.request = Request.objects.create(
            # Must be in the form YYYY-MM-DD
            username = self.user,
            availability_date = "2022-12-29",
            availability_time = "08:30",
            instrument = "violin",
            interval_between_lessons = 5,
            number_of_lessons = 5,
            duration_of_lessons = 30
        )

        self.delete_url = reverse('delete-request', kwargs={'id': self.request.id})
        self.update_url = reverse('update-request', kwargs={'id': self.request.id})


    def test_delete_request_url(self):
        self.assertEqual(self.delete_url,f'/delete_request/{self.request.id}')

    def test_update_request_url(self):
        self.assertEqual(self.update_url,f'/update_request/{self.request.id}')

    def test_delete_request_after_toggle(self):
        self.client.login(username = self.user.username, password='Password123')
        requests_before = len(Request.objects.values())
        self.client.get(self.delete_url, follow=True)
        requests_after = len(Request.objects.values())
        self.assertEquals(requests_before, requests_after+1)
    

    def test_update_request_after_toggle(self):
        self.client.login(username = self.user.username, password='Password123')
        requests_before = len(Request.objects.values())
        self.client.get(self.update_url, follow=True)
        requests_after = len(Request.objects.values())
        self.assertEquals(requests_before, requests_after)