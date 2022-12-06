from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django import forms
from lessons.forms import TermForm
from lessons.models import Term
from django.urls import reverse
import datetime
from lessons.models import User, Term
class DeleteTermViewTestCase(TestCase):
    """Unit tests for the Term deletion view."""

    fixtures = [
        'lessons/tests/fixtures/terms.json',
        'lessons/tests/fixtures/default_admin.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username = "danielthomas@example.com")
        self.client.login(username=self.user.username, password="Password123")

        self.term = Term.objects.get(id=1)
        self.url = reverse("admin_delete_term", args=[self.term.id])


    def test_term_url(self):
        self.assertEqual(self.url, "/admin/delete_term/" + str(self.term.id))


    def test_get_term_deletion_page(self):
        response = self.client.get(self.url)
        response_url = reverse("admin_view_terms")
        self.assertRedirects(response, response_url, status_code=302,target_status_code=200)


    def test_deletion(self):
        before_count = Term.objects.count()
        response = self.client.post(self.url)
        after_count = Term.objects.count()
        self.assertEqual(after_count, before_count-1)
        response_url = reverse("admin_view_terms")
        self.assertRedirects(response, response_url, status_code=302,target_status_code=200)
