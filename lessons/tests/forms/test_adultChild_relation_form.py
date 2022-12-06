from django.test import TestCase
from django import forms
from lessons.forms import AdultChildRelationForm
from lessons.models import User, Adult, AdultChildRelationship
from django.contrib.auth.hashers import check_password

class CreateAdultChildRelationshipFormTestCase(TestCase):
    """Unit tests for adult child relationship form"""

    fixtures = [
        "lessons/tests/fixtures/default_adult.json",
        "lessons/tests/fixtures/default_children.json"
    ]


    def setUp(self):
        self.adult = Adult.objects.get(pk=1)
        self.child = User.objects.get(pk=2)
        self.child2 = User.objects.get(pk=3)

        self.form_input = {
            "adult" : self.adult,
            "child" : self.child
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

        new_form_input = {
            "adult" : self.adult,
            "child" : self.child2
        }

        form2 = AdultChildRelationForm(data=new_form_input)
        self.assertTrue(form.is_valid())
        before = AdultChildRelationship.objects.count()
        form.save()
        form2.save()

        after = AdultChildRelationship.objects.count()
        self.assertEqual(before+2, after)

    def test_cannot_add_same_child(self):
        form = AdultChildRelationForm(data=self.form_input)
        form2 = AdultChildRelationForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        before = AdultChildRelationship.objects.count()
        with self.assertRaises(ValueError):
            form.save()
            form2.save()
        after = AdultChildRelationship.objects.count()
        self.assertEqual(before+1, after)

    def test_get_valid_child_from_relation(self):
        form = AdultChildRelationForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        form.save()
        rel = AdultChildRelationship.objects.get(adult=self.adult,child=self.child)

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
        with self.assertRaises(ValueError):
            form = AdultChildRelationForm(data=self.form_input)
            form.save()

    def test_set_self_as_child(self):
        self.form_input["child"] = "none@michael.kolling@kcl.ac.uk"
        with self.assertRaises(ValueError):
            form = AdultChildRelationForm(data=self.form_input)
            form.save()
