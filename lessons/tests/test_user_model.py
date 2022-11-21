from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import User

class UnitModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name = 'Michael',
            last_name = 'Kolling',
            username = 'michael.kolling@kcl.ac.uk',
            password = 'password123'
        )

    def test_valid_user(self):
        self._assert_user_is_valid();

    #first name

    def test_first_name_cannot_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid();

    def test_first_name_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid();

    def test_first_name_can_be_50_characters_long(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid();

    def test_first_name_cannot_be_51_characters_long(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid();

    #last name

    def test_last_name_cannot_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid();

    def test_last_name_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid();

    def test_last_name_can_be_50_characters_long(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid();

    def test_last_name_cannot_be_51_characters_long(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid();

    #email

    def test_email_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid();

    def test_email_must_be_unique(self):
        second_user = self._create_second_user()
        self.user.username = second_user.email
        self._assert_user_is_invalid();

    def test_email_must_contain_a_username(self):
        self.user.username = '@kcl.ac.uk'
        self._assert_user_is_invalid();

    def test_email_must_contain_at_symbol(self):
        self.user.username = 'michaelkollingkcl.ac.uk'
        self._assert_user_is_invalid();

    def test_email_must_contain_domain_name(self):
        self.user.username = 'michaelkolling@.uk'
        self._assert_user_is_invalid();

    def test_email_must_contain_domain(self):
        self.user.username = 'michaelkolling@kcl'
        self._assert_user_is_invalid();

    def test_email_must_not_contain_more_than_one_at_symbol(self):
        self.user.username = 'michaelkolling@@kcl.ac.uk'
        self._assert_user_is_invalid();

    def test_email_may_contain_more_than_one_dot(self):
        self.user.username = 'michaelkolling@kcl.ac.uk'
        self._assert_user_is_valid();


    #user validation

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid.')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def _create_second_user(self):
        user = User.objects.create_user(
            first_name = 'Josh',
            last_name = 'Murphy',
            username='josh.murphy@kcl.ac.uk',
            password='password123',
        )
        return user
