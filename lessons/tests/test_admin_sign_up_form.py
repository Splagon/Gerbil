from django.test import TestCase
from django import forms
from lessons.forms import AdminSignUpForm
from ..models import User
from django.contrib.auth.hashers import check_password

class AdminSignUpFormTestCase(TestCase):
    """Unit tests for sign-up form"""
    def setUp(self):
        self.form_input = {
            "first_name": "Harry",
            "last_name": "Kane",
            "username": "harry.kane@england.co.uk",
            "dateOfBirth": "01/01/1995",
            "password" : "Password123",
            "password_confirm" : "Password123",
            "is_superuser" : False,
            "balance": 0.0
        }

    # Form accepts valid input data
    def test_valid_sign_up_form(self):
        form = AdminSignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    # Form has necessary fields
    def test_form_has_necessary_fields(self):
        form = AdminSignUpForm()

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

        self.assertIn("is_superuser", form.fields)
        superuser_wdg = form.fields["is_superuser"].widget
        self.assertTrue(isinstance(superuser_wdg, forms.CheckboxInput))



    # Form uses model validation
    def test_form_uses_model_validation(self):
        self.form_input["username"] = ""
        form = AdminSignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # New password has correct format
    def test_password_must_contain_uppercase(self):
        self.form_input["password"] = "password123"
        self.form_input["password_confirm"] = "password123"
        form=AdminSignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase(self):
        self.form_input["password"] = "PASSWORD123"
        self.form_input["password_confirm"] = "PASSWORD123"
        form=AdminSignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input["password"] = "PasswordABC"
        self.form_input["password_confirm"] = "PasswordABC"
        form=AdminSignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_passwords_must_be_identical(self):
        self.form_input["password_confirm"] = "WrongPass123"
        form=AdminSignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    # Validates incorrect date of birth
    def test_dob_no_entry(self):
        self.form_input["dateOfBirth"] = ""
        form=AdminSignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_dob_invalid(self):
        self.form_input["dateOfBirth"] = "NotAValidDate123"
        form=AdminSignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    def test_form_must_save_correctly(self):
        form=AdminSignUpForm(data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count+1)

        user = User.objects.get(username="harry.kane@england.co.uk")
        self.assertEqual(user.first_name, "Harry")
        self.assertEqual(user.last_name, "Kane")
        self.assertEqual(user.username, "harry.kane@england.co.uk")
        self.assertEqual(user.dateOfBirth.strftime("%d/%m/%Y"), "01/01/1995")
        is_pass_correct = check_password("Password123", user.password)
        self.assertTrue(is_pass_correct)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, False)
