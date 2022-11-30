"""Tests of the log in view."""
from django.test import TestCase
from django.urls import reverse
from lessons.forms import LogInForm
from lessons.models import User
from .helpers import LogInTester

class LogInViewTestCase(TestCase, LogInTester):
    """Tests of the log in view."""



    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.create_user(username ="johndoe@example.org",

            first_name= 'John',
            last_name= 'Doe',
            #'username': '@janedoe',
            password = "Password123",
            is_active=True,
            id = "3"


            #'new_password': 'Password123',
            #'password_confirmation': 'Password123'
        )


    def test_log_in_url(self):
        self.assertEqual(self.url,'/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_log_in(self):
        form_input = { "username": "johndoe@example.org", "password": "WrongPassword123"}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_succesful_log_in(self):
        form_input = { "username": "johndoe@example.org", "password": "Password123"}
        response = self.client.post(self.url, form_input, follow = True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')

    def test_valid_log_in_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = { "username": "johndoe@example.org", "password": "Password123"}
        response = self.client.post(self.url, form_input, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
