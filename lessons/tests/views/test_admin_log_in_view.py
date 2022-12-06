"""Tests of the sign up view."""
from django.test import TestCase
from django.urls import reverse
from lessons.forms import LogInForm
from lessons.models import User
from ..helpers import LogInTester

class LogInViewTestCase(TestCase, LogInTester):
    """Tests of the log in view."""

    fixtures = ["lessons/tests/fixtures/default_user.json"]

    def setUp(self):
        self.url = reverse('admin_log_in')
        self.user = User.objects.get(username="jonathandeer@example.com")


    def test_log_in_url(self):
        self.assertEqual(self.url,'/admin/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/admin_log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_log_in(self):
        form_input = { "username": self.user.username, "password": "WrongPassword123"}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/admin_log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_succesful_log_in(self):
        form_input = { "username": self.user.username, "password": "Password123"}
        response = self.client.post(self.url, form_input, follow = True)
        self.assertTrue(self._is_logged_in())
        #To do
        #These 3 lines of code need to be chnaged () when  the  view for the
        #page that goes after the log in one  is implemented (when this is done,
        # replace  the word "feed" in line 61 and 63  with whatever the name of your view is ")

        response_url = reverse('admin_home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'admin/admin_home.html')

    def test_valid_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = { "username": self.user.username, "password": "Password123"}
        response = self.client.post(self.url, form_input, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/admin_log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
