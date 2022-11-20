from django.test import TestCase
from django import forms
from django.core.exceptions import ValidationError
from ..models import User
from lessons.forms import SignUpForm

class UnitModelTestCase(TestCase):
    """Unit tests for sign-up form"""
    def setUp(self):
        self.form_input = {
            "first_name": "Michael",
            "last_name": "Kolling",
            "username": "michael.kolling@kcl.ac.uk",
            "password" : "Password123",
            "password_confirm" : "Password123"
        }
    
    # Form accepts valid input data
    def test_valid_sign_up_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    # Form has necessary fields
    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        
        self.assertIn("username", form.fields)
        user_email_field = form.fields["username"]
        self.assertTrue(isinstance(user_email_field, forms.EmailField))
        
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        
        self.assertIn("dateOfBirth", form.fields)
        user_date_field = form.fields["dateOfBirth"]
        self.assertTrue(isinstance(user_date_field, forms.DateField))
        
        self.assertIn("password", form.fields)
        password_wdg = form.fields["password"].widget
        self.assertTrue(isinstance(password_wdg, forms.PasswordInput))
        
        self.assertIn("password_confirm", form.fields)
        password_wdg = form.fields["password_confirm"].widget
        self.assertTrue(isinstance(password_wdg, forms.PasswordInput))
        
        
    
    # Form uses model validation
    def test_form_uses_model_validation(self):
        self.form_input["username"] = ""
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    # New password has correct format
    def test_password_must_contain_uppercase(self):
        self.form_input["password"] = "password123"
        self.form_input["password_confirm"] = "password123"
        form=SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_password_must_contain_lowercase(self):
        self.form_input["password"] = "PASSWORD123"
        self.form_input["password_confirm"] = "PASSWORD123"
        form=SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
          
    def test_password_must_contain_number(self):
        self.form_input["password"] = "PasswordABC"
        self.form_input["password_confirm"] = "PasswordABC"
        form=SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        
    def test_passwords_must_be_identical(self):
        self.form_input["password_confirm"] = "WrongPass123"
        form=SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())