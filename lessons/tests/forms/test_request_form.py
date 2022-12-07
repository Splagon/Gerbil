"""Unit tests of the request form."""
from django import forms
from django.test import TestCase
from lessons.forms import RequestForm
from lessons.models import Request
from lessons.models import User
import datetime
class RequestFormTestCase(TestCase):
    """Unit tests of the request form."""

    # Get user to identify request form
    fixtures = [
        'lessons/tests/fixtures/default_user2.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='michael.kolling@kcl.ac.uk')
        self.form_input = {
            'availability_date': datetime.date.today(),
            'availability_time': '09:00',
            'duration_of_lessons': 30,
            'interval_between_lessons': 1,
            # 'number_of_lessons': 2,
            'instrument': 'Violin',
            'teacher': 'Mr Doe'
        }



    def test_form_has_necessary_fields(self):
        form = RequestForm()
        self.assertIn('availability_date', form.fields)
        availability_date_field = form.fields['availability_date']
        self.assertTrue(isinstance(availability_date_field, forms.DateField))

        self.assertIn('availability_time', form.fields)
        availability_time_field = form.fields['availability_time']
        self.assertTrue(isinstance(availability_time_field, forms.TimeField))

        self.assertIn('duration_of_lessons', form.fields)
        duration_of_lessons_widget = form.fields['duration_of_lessons'].widget
        self.assertTrue(isinstance(duration_of_lessons_widget, forms.Select))

        self.assertIn('interval_between_lessons', form.fields)
        # self.assertIn('number_of_lessons', form.fields)

    def test_valid_request_form_(self):
        form = RequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())


    def test_request_form_must_save_correctly(self):
        form=RequestForm(data=self.form_input)
        before_count = Request.objects.count()
        form.save(self.user)
        after_count = Request.objects.count()
        self.assertEqual(after_count, before_count+1)
        request = Request.objects.get(username=self.user)
        self.assertEqual(request.availability_time.strftime('%H:%M'), "09:00")
        self.assertEqual(request.duration_of_lessons, '30')
        self.assertEqual(request.interval_between_lessons, '1')
        self.assertEqual(request.instrument, 'Violin')
        self.assertEqual(request.teacher,'Mr Doe')
