from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django import forms
from lessons.forms import TermForm
from lessons.models import Term
from django.urls import reverse
import datetime
from lessons.models import User, Term
class EditTermViewTestCase(TestCase):
    """Unit tests for the Term editing view."""

    fixtures = [
        'lessons/tests/fixtures/terms.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username = "danielthomas@example.com")
        self.client.login(username=self.user.username, password="Password123")

        self.term = Term.objects.get(id=1)
        self.url = reverse("admin_edit_term", args=[self.term.id])


    def test_term_url(self):
        self.assertEqual(self.url, "/admin/edit_term/" + str(self.term.id))


    def test_get_term_editing_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/admin_edit_term.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, TermForm))
        self.assertFalse(form.is_bound)


    def test_unsuccessful_term_edit_via_model_constraints(self):
        self.form_input = {
            "startDate": "2023-3-31",
            "endDate": "2023-3-01"
        }
        before_count = Term.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Term.objects.count()
        self.assertEqual(after_count, before_count)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/admin_edit_term.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form,TermForm))
        self.assertTrue(form.is_bound)


    def test_unsuccessful_term_edit_due_to_other_conflicting_term_dates(self):
        self.form_input = {
            "startDate": "2023-1-15",
            "endDate": "2023-2-15"
        }
        before_count = Term.objects.count()
        response = self.client.post(self.url, self.form_input, )
        after_count = Term.objects.count()
        self.assertEqual(after_count, before_count)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/admin_edit_term.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form,TermForm))
        self.assertTrue(form.is_bound)


    def test_successful_term_edit(self):
        self.form_input = {
            "startDate": "2023-03-01",
            "endDate": "2023-03-31"
        }
        response = self.client.post(self.url, self.form_input, follow=True, kwargs = {'id': self.term.id})
        after_edit = Term.objects.get(id=self.term.id)
        self.assertTrue(str(after_edit.startDate) == self.form_input.get('startDate') and str(after_edit.endDate) == self.form_input.get('endDate'))
        response_url = reverse("admin_view_terms")
        self.assertRedirects(response, response_url, status_code=302,target_status_code=200)
        self.assertTemplateUsed(response, "admin/admin_view_terms.html")
