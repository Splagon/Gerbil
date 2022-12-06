"""Unit tests of the request form."""
from django import forms
from django.test import TestCase
from lessons.forms import TermForm
from lessons.models import Term
import datetime
class TermFormTestCase(TestCase):
    """Unit tests of the request form."""

    fixtures = ['lessons/tests/fixtures/terms.json']

    def setUp(self):
        self.form_input = {
            "startDate": "2024-2-1",
            "endDate": "2024-3-31"
        }

    def test_valid_term_form(self):
        form = TermForm(data=self.form_input)
        self.assertTrue(form.is_valid())


    def test_form_has_necessary_fields(self):
        form = TermForm()

        self.assertIn('startDate', form.fields)
        startDate = form.fields['startDate']
        self.assertTrue(isinstance(startDate, forms.DateField))

        self.assertIn('endDate', form.fields)
        endDate = form.fields['endDate']
        self.assertTrue(isinstance(endDate, forms.DateField))


    def end_date_may_not_be_before_the_start_date(self):
        self.form_input = {
            "startDate": "2023-1-31",
            "endDate": "2023-1-1"
        }
        test_valid_term_form()


    def test_new_term_must_not_overlap_existing_term(self):
        self.term = Term.objects.get(pk=1)
        self.form_input = {
            "startDate": "2023-01-05",
            "endDate": "2023-01-25"
        }
        form = TermForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    def test_term_may_be_edited_without_overlaps_of_existing_terms(self):
        self.id = 1
        self.term = Term.objects.get(pk=self.id)
        self.form_input = {
            "startDate": "2023-01-05",
            "endDate": "2023-01-25"
        }
        form = TermForm(data=self.form_input, idNum=self.id)
        self.assertTrue(form.is_valid())

        self.term.startDate = form.cleaned_data.get('startDate')
        self.term.endDate = form.cleaned_data.get('endDate')
        self.term.save()

        self.assertTrue(str(self.term.startDate) == self.form_input.get('startDate') and str(self.term.endDate) == self.form_input.get('endDate'))


    def test_term_may_not_be_edited_with_overlaps_of_existing_terms(self):
        self.id = 1
        self.term = Term.objects.get(pk=self.id)
        self.form_input = {
            "startDate": "2023-1-15",
            "endDate": "2023-2-15"
        }
        form = TermForm(data=self.form_input, idNum=self.id)
        self.assertFalse(form.is_valid())
