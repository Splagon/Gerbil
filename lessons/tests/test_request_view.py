"""Tests of the feed view."""
from django.test import TestCase
from django.urls import reverse
from lessons.forms import RequestForm
from lessons.models import User
from lessons.tests.helpers import create_requests, reverse_with_next

class RequestViewTestCase(TestCase):
    """Tests of the request view."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='jonathandeer@example.com')
        self.url = reverse('requests')

    def test_requests_url(self):
        self.assertEqual(self.url,'/requests/')

    def test_get_request(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requests.html')
        form = response.context
        print(form)
        # self.assertTrue(isinstance(form, RequestForm))
        # self.assertFalse(form.is_bound)



    def test_login_required(self):
        response = self.client.get(reverse('requests'))
        self.assertRedirects(response, reverse('log_in')+'?next=/requests/')

    
