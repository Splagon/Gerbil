"""Unit tests of the request form."""
from django import forms
from django.test import TestCase
from lessons.forms import RequestForm
import datetime
class RequestFormTestCase(TestCase):
    """Unit tests of the request form."""


    def setUp(self):
        self.form_input = {
            'availability_date': datetime.date.today(),
            'availability_time': '09:00',
            'duration_of_lessons': 30,
            'interval_between_lessons': 5,
            'number_of_lessons': 2,
            'instrument': 'violin',
            'teacher': 'Mr Doe'
        }
    
    def test_valid_sign_up_form(self):
        form = RequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())

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
        self.assertIn('number_of_lessons', form.fields)
       
    def test_time_must_be_after_eight(self):
        self.form_input['availability_time'] = '03:00'
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    



    def test_time_must_be_before_five_thirty(self):
        self.form_input['availability_time'] = '17:31'
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_teacher_must_be_not_be_overlong(self):
        self.form_input['teacher'] = 'a' * 51
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_availability_date_must_not_be_before_today(self):
        tod = datetime.datetime.today()
        d = datetime.timedelta(days=5)

        self.form_input['availability_date'] = tod - d
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_availability_date_must_not_be_after_two_years(self):
        tod = datetime.datetime.today()
        d = datetime.timedelta(days=365 * 2)
        self.form_input['availability_date'] = tod + d
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_availability_date_can_be_after_one_year(self):
        tod = datetime.datetime.today()
        d = datetime.timedelta(days=365 )

        self.form_input['availability_date'] = tod + d
        form = RequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())


    def test_interval_between_lessons_must_not_be_blank(self):
        self.form_input['interval_between_lessons'] = ''
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_duration_of_lessons_must_not_be_blank(self):
        self.form_input['duration_of_lessons'] = ''
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_number_of_lessons_must_not_be_blank(self):
        self.form_input['number_of_lessons'] = ''
        form = RequestForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_instrument_can_be_blank(self):
        self.form_input['instrument'] = ()
        form = RequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_teacher_can_be_blank(self):
        self.form_input['teacher'] = ()
        form = RequestForm(data=self.form_input)
        self.assertTrue(form.is_valid())

   