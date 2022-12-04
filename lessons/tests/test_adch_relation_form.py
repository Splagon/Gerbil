from django.test import TestCase
from django import forms
from lessons.forms import AdultChildRelationForm
from ..models import User, Adult, AdultChildRelationship
from django.contrib.auth.hashers import check_password

class SignUpFormTestCase(TestCase):
    """Unit tests for adult child relationship form"""
    def setUp(self):
        self.adult = Adult.objects.create_user(
            first_name = "Michael",
            last_name = "Kolling",
            username= "michael.kolling@kcl.ac.uk",
            dateOfBirth="1995-01-01",
            password = "Password123",
            is_adult = True
        )
        self.child = User.objects.create_user(
            first_name = "Jimmy",
            last_name = "John",
            username= "jimmy.john@kcl.ac.uk",
            dateOfBirth="2007-01-01",
            password = "Password123", 
            is_adult = False
        )
        self.form_input = {
            "adult" : self.adult,
            "child" : "jimmy.john@kcl.ac.uk"
        }
        
    def test_create_valid_relationship(self):
        form = AdultChildRelationForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_invalid_relation_no_child(self):
        self.form_input["child"] = ""
        form = AdultChildRelationForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_relation_no_adult(self):
        self.form_input["adult"] = ""
        form = AdultChildRelationForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_relationship_made(self):
        form = AdultChildRelationForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        before = AdultChildRelationship.objects.count()
        form.save()
        after = AdultChildRelationship.objects.count()
        self.assertEqual(before+1, after)
    
    def test_multiple_children(self):
        form = AdultChildRelationForm(data=self.form_input)
        self.form_input["child"] = "none@none.org" # does not exist
        form2 = AdultChildRelationForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        before = AdultChildRelationship.objects.count()
        form.save()
        form2.save()
        after = AdultChildRelationship.objects.count()
        self.assertEqual(before+2, after)
    
    def test_get_valid_child_from_relation(self):
        form = AdultChildRelationForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        form.save()
        rel = AdultChildRelationship.objects.get(adult=self.adult,child="jimmy.john@kcl.ac.uk")
        
        child = User.objects.get(username=rel.child)
        self.assertEqual(child.username, "jimmy.john@kcl.ac.uk")
        self.assertEqual(child.first_name, "Jimmy")
        self.assertEqual(child.last_name, "John")
        self.assertEqual(child.dateOfBirth.strftime("%Y-%m-%d"), "2007-01-01")
        is_pass_correct = check_password("Password123", child.password)
        self.assertTrue(is_pass_correct)
        self.assertEqual(child.is_adult, False)
    
    def test_get_invalid_child_from_relation(self):
        self.form_input["child"] = "none@none.org"
        form = AdultChildRelationForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        form.save()
        rel = AdultChildRelationship.objects.get(adult=self.adult,child="none@none.org")
        
        self.assertFalse(User.objects.filter(username=rel.child).exists())