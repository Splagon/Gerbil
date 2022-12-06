from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import User, Adult, AdultChildRelationship

class AdultModelTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_adult.json',
        'lessons/tests/fixtures/default_children.json'
    ]

    def setUp(self):
        self.adult = Adult.objects.get(pk=1)
        self.child = User.objects.get(pk=2)
        self.relation = AdultChildRelationship.objects.create(
            adult=self.adult,
            child=self.child
        )


    def test_valid_adult(self):
        try:
            self.adult.full_clean()
        except (ValidationError):
            self.fail('Test adult should be valid.')

    def test_valid_child(self):
        try:
            self.child.full_clean()
        except (ValidationError):
            self.fail('Test child should be valid.')

    def test_create_relationship(self):
        try:
            self.relation.full_clean()
        except (ValidationError):
            self.fail('Test relation should be valid.')

    def test_create_invalid_relationship_no_child(self):
        self.relation.child = None
        with self.assertRaises(ValidationError):
            self.relation.full_clean()

    def test_create_invalid_relationship_no_adult(self):
        self.relation.adult = None
        with self.assertRaises(ValidationError):
            self.relation.full_clean()

    def test_delete_adult_delete_relation(self):
        self.adult.delete()
        self._assert_relation_unfindable()

    def test_child_is_actual_user(self):
        self.assertEqual(User.objects.get(id=self.relation.child.id), self.child)


    def _assert_relation_unfindable(self):
        counter = 0
        for c in AdultChildRelationship.objects.all():
            if c.adult == self.adult:
                counter += 1
        if counter == 0:
            return True
        return False
