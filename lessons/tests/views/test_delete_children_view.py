from django.test import TestCase
from django import forms
from lessons.forms import AdultChildRelationForm
from django.urls import reverse
from lessons.models import User, Adult, AdultChildRelationship
from django.contrib.auth.hashers import check_password

class DeleteChildViewTestCase(TestCase):
    
    fixtures = ["lessons/tests/fixtures/default_children.json"]
    
    def setUp(self):
        
        self.adult = Adult.objects.create_user(
            first_name = "Michael",
            last_name = "Kolling",
            username= "michael.kolling@kcl.ac.uk",
            dateOfBirth="1995-01-01",
            password = "Password123",
            is_adult = True
        )
        
        self.child = User.objects.get(username="jimmy.john@kcl.ac.uk")
        
        """Dynamic url requires use of kwargs"""
        self.url = reverse("delete_child", kwargs={"child_id":self.child.id})
        
        self.relation = AdultChildRelationship.objects.create(
            adult = self.adult,
            child = self.child
        )
        
        self.client.login(username=self.adult.username,password="Password123")
        
    def test_view_child_url(self):
        """Tests that reverse gives the correct dynamic url"""
        self.assertEqual(self.url,"/delete_child/" + str(self.child.id))
    
    def test_delete_child(self):
        """Deleting a child should remove the associated
        AdultChildRelationship object and redirect back to
        view_children"""
        before_count = AdultChildRelationship.objects.count()
        response = self.client.get(self.url)
        response_url = reverse("view_children")
        self.assertRedirects(response, response_url, status_code=302,target_status_code=200)
        after_count = AdultChildRelationship.objects.count()
        self.assertNotEqual(before_count, after_count)
        self.assertEqual(before_count-1, after_count)
        
    
    
    
    