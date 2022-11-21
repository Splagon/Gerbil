"""Unit tests of the login form"""
from django import forms
from django.test import TestCase
from lessons.models import RequestForm
from django.utils.timezone import now


class RequestFormTestCase(TestCase):
    """Unit tests of the request form"""

    def setUp(self):
        self.form_input = {
            # Slots the student is available for
            'availability': '2001-12-1',
            # Number of lessons that student wants
            'number_of_lessons': '5',
            # This is measured in days
            'interval_between_lessons': '4',
            # This is measured in minutes
            'duration_of_lessons': '50',
            # What they want to learn
            'instrument': ('violin', 'violin'),
            # Teacher name
            'teacher': 'Mr Doe'

        }

    def test_form_contains_required_fields(self):
        form = RequestForm()
        self.assertIn('availability', form.fields)
        self.assertIn('number_of_lessons', form.fields)
        self.assertIn('interval_between_lessons', form.fields)
        self.assertIn('duration_of_lessons', form.fields)

        # availability_field = form.fields['availability']
        # self.assertTrue(isinstance(
        #     availability_field.widget, forms.DateField))

    def test_form_accepts_valid_input(self):
        form = RequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_availability(self):
        self.form_input['availability'] = []
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_number_of_lessons(self):
        self.form_input['number_of_lessons'] = ''
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_interval_between_lessons(self):
        self.form_input['interval_between_lessons'] = ''
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_duration_of_lesson(self):
        self.form_input['duration_of_lessons'] = ''
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accept_blank_instrument(self):
        self.form_input['instrument'] = ("", "")
        form = RequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accept_blank_teacher(self):
        self.form_input['teacher'] = ''
        form = RequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Checking any of the dates given in the availability list is after current date
    # def test_availability_dates_after_current_date(self):
    #     for date in self.form_input['availability']:
