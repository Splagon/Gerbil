from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django import forms
from lessons.forms import TermForm
from lessons.models import Term
from django.urls import reverse
import datetime
from lessons.models import User, Term
class TermViewTestCase(TestCase):
    """Unit tests for the Term editing view."""

    fixtures = [
        'lessons/tests/fixtures/terms.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username = "danielthomas@example.com")
        self.client.login(username=self.user.username, password="Password123")
        self.url = reverse("admin_add_term")

    def test_term_url(self):
        self.assertEqual(self.url,"/admin/add_term/")


    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/admin_add_term.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form, TermForm))
        self.assertFalse(form.is_bound)


    def test_unsuccessful_term_addition(self):
        self.form_input = {
            "startDate": "2023-03-31",
            "endDate": "2023-03-01"
        }
        before_count = Term.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Term.objects.count()
        self.assertEqual(after_count, before_count)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/admin_add_term.html")
        form = response.context["form"]
        self.assertTrue(isinstance(form,TermForm))
        self.assertTrue(form.is_bound)


    def test_successful_term_addition(self):
        self.form_input = {
            "startDate": "2023-03-01",
            "endDate": "2023-03-31"
        }
        before_count = Term.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Term.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse("admin_view_terms")
        self.assertRedirects(response, response_url, status_code=302,target_status_code=200)
        self.assertTemplateUsed(response, "admin/admin_view_terms.html")
