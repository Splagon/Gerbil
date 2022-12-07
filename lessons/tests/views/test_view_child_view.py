from django.test import TestCase
from django import forms
from lessons.forms import AdultChildRelationForm
from django.urls import reverse
from lessons.models import User, Adult, AdultChildRelationship
from django.contrib.auth.hashers import check_password

class ViewChildViewTestCase(TestCase):
    
    fixtures = ["lessons/tests/fixtures/default_children.json"]
    
    def setUp(self):
        self.url = reverse("view_children")
        self.adult = Adult.objects.create_user(
            first_name = "Michael",
            last_name = "Kolling",
            username= "michael.kolling@kcl.ac.uk",
            dateOfBirth="1995-01-01",
            password = "Password123",
            is_adult = True
        )
        self.child = User.objects.get(username="jimmy.john@kcl.ac.uk")
        self.relation = AdultChildRelationship.objects.create(
            adult = self.adult,
            child = self.child
        )
        
        self.client.login(username=self.adult.username,password="Password123")
        
    def test_view_child_url(self):
        self.assertEqual(self.url,"/view_children/")
    
    def test_get_array_children(self):
        """Attempt to get children array; there should only be 1 child"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "view_children.html")
        child_array = response.context["children"]
        self.assertEqual(len(child_array), 1)