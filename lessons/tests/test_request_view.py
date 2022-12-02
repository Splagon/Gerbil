"""Tests of the feed view."""
from django.test import TestCase
from django.urls import reverse
from lessons.forms import RequestForm
from lessons.models import User, Request
from lessons.tests.helpers import create_requests, reverse_with_next

class RequestViewTestCase(TestCase):
    """Tests of the request view."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json'
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
        
    def test_get_request_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_login_required(self):
        response = self.client.get(reverse('requests'))
        self.assertRedirects(response, reverse('log_in')+'?next=/requests/')

    
    def test_request_created_with_teachers(self):
        self.client.login(username=self.user.username, password='Password123')
        phil = User.objects.get(username='phildunphy@email.com')
        create_requests(self.user, 100, 103)
        create_requests(phil, 200, 203)
        # create_requests(claire, 300, 303)
        # create_requests(cameron, 400, 403)


        philRequest = Request.objects.all().values()
        first_request = philRequest.filter(teacher="Request__200")
        self.assertTrue(first_request[0]['teacher'], 'Request__200')
        # claireRequest = Request.objects.get(username = claire)
        # cameronRequest = Request.objects.get(username = cameron)
        
        # for request in philRequest:
        #     self.assertContains(request['teacher'], f'Request__100')
        # for count in range(200, 203):
        #     self.assertContains(response, f'Post__{count}')
        # for count in range(300, 303):
        #     self.assertContains(response, f'Post__{count}')
        # for count in range(400, 403):
        #     self.assertNotContains(response, f'Post__{count}')