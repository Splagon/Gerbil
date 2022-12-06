"""Unit tests of the log in form."""
from django import forms
from django.test import TestCase
from lessons.models import User
from lessons.forms import LogInForm

class LogInFormTestCase(TestCase):
    """Unit tests of the log in form"""

    fixtures = [
        'lessons/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        #self.user = User.objects.get(username='jonathandeer@example.com@example.com')
        self.form_input = {"username": "jonathandeer@example.com",
         "password": "pbkdf2_sha256$260000$4BNvFuAWoTT1XVU8D6hCay$KqDCG+bHl8TwYcvA60SGhOMluAheVOnF1PMz0wClilc="}


    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn("username", form.fields)
        self.assertIn("password", form.fields)
        password_field = form.fields["password"]
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_username(self):
        self.form_input['username'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_incorrect_username(self):
        self.form_input['username'] = 'ja'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'zyzz'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())
