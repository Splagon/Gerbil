"""Tests of the feed view."""
from django.test import TestCase
from django.urls import reverse
from lessons.forms import RequestForm
from lessons.models import User
from lessons.tests.helpers import create_requests, reverse_with_next


class RequestFormViewTestCase(TestCase):
    """Tests of the request form view."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='jonathandeer@example.com')
        self.url = reverse('request_form')

    def test_request_url(self):
        self.assertEqual(self.url,'/request-lesson/')

    def test_get_request(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'request_form.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RequestForm))
        self.assertFalse(form.is_bound)
    
    def test_get_request_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('requests')
        self.assertTemplateUsed(response, 'request_form.html')