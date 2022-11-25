import datetime
from django import forms
from django.test import TestCase
from lessons.forms import UserForm
from lessons.models import User


class UserFormTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.form_input = {
            'username': 'bobsmith@email.com',
            'first_name': 'Bob',
            'last_name': 'Smith',
            'dateOfBirth': '2000-01-01'
        }

    def test_form_has_necessary_fields(self):
        form = UserForm()
        self.assertIn('username', form.fields)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('dateOfBirth', form.fields)
        dateOfBirth_field = form.fields['dateOfBirth']
        self.assertTrue(isinstance(dateOfBirth_field, forms.DateField))

    def test_valid_user_form(self):
        form = UserForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'badusername' #no @ sign which is needed
        form = UserForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        user = User.objects.get(username='michael.kolling@kcl.ac.uk')
        form = UserForm(instance=user, data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(user.username, 'bobsmith@email.com')
        self.assertEqual(user.first_name, 'Bob')
        self.assertEqual(user.last_name, 'Smith')
        self.assertEqual(user.dateOfBirth, datetime.date(2000, 1, 1))
