from django.test import TestCase
from django import forms
from lessons.forms import AdultChildRelationForm
from django.urls import reverse
from lessons.models import User, Adult, AdultChildRelationship, Request
from django.contrib.auth.hashers import check_password

class RequestFormChildViewTestCase(TestCase):
    
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
        self.url = reverse("request_form_child", kwargs={"child_id":self.child.id})
        
        self.relation = AdultChildRelationship.objects.create(
            adult = self.adult,
            child = self.child
        )
        
        self.form_input = {
            "username" : self.child.username,
            "availability_date":"2022-12-29",
            "availability_time":"08:30",
            "instrument":"Violin",
            "interval_between_lessons": 1,
            "duration_of_lessons":30
        }
        
        self.client.login(username=self.adult.username,password="Password123")
    
    def test_request_form_child_url(self):
        """Tests that reverse gives the correct dynamic url"""
        self.assertEqual(self.url,"/request_form_child/" + str(self.child.id))
        
    def test_submit_valid_form_for_child(self):
        before_count = Request.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse("view_children")
        self.assertRedirects(response, response_url, status_code=302,target_status_code=200)
        after_count = Request.objects.count()
        self.assertEqual(after_count, before_count+1)