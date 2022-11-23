import datetime
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from lessons.forms import UserForm
from lessons.models import User 
# from microblogs.tests.helpers import create_posts, reverse_with_next


class ProfileViewTest(TestCase):
    """Test suite for the profile view."""

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='michael.kolling@kcl.ac.uk')
        self.url = reverse('profile')
        self.form_input = {
            'first_name': 'Michael2',
            'last_name': 'Kolling2',
            'username': 'michael.kolling2@kcl.ac.uk',
            'dateOfBirth': '2000-02-02'
        }

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    def test_get_profile(self):
        # self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertEqual(form.instance, self.user)

    # def test_get_profile_redirects_when_not_logged_in(self):
    #     redirect_url = reverse_with_next('log_in', self.url)
    #     response = self.client.get(self.url)
    #     self.assertRedirects(response, redirect_url,
    #                         status_code=302, target_status_code=200)

    def test_unsuccesful_profile_update(self):
        # self.client.login(username=self.user.username, password='Password123')
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'michael.kolling@kcl.ac.uk')
        self.assertEqual(self.user.first_name, 'Michael')
        self.assertEqual(self.user.last_name, 'Kolling')
        self.assertEqual(self.user.dateOfBirth, datetime.date(1995, 1, 1))

    def test_unsuccessful_profile_update_due_to_duplicate_username(self):
        # self.client.login(username=self.user.username, password='Password123')
        # this usrname already exists from other_users.json
        self.form_input['username'] = 'phildunphy@email.com'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'michael.kolling@kcl.ac.uk')
        self.assertEqual(self.user.first_name, 'Michael')
        self.assertEqual(self.user.last_name, 'Kolling')
        self.assertEqual(self.user.dateOfBirth, datetime.date(1995, 1, 1))

    def test_succesful_profile_update(self):
        # self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('lessons')  # redirects to correct page
        self.assertRedirects(response, response_url,
                            status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'lessons.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'michael.kolling2@kcl.ac.uk')
        self.assertEqual(self.user.first_name, 'Michael2')
        self.assertEqual(self.user.last_name, 'Kolling2')
        self.assertEqual(self.user.dateOfBirth, datetime.date(2000, 2, 2))

    # def test_post_profile_redirects_when_not_logged_in(self):
    #     redirect_url = reverse_with_next('log_in', self.url)
    #     response = self.client.post(self.url, self.form_input)
    #     self.assertRedirects(response, redirect_url,
    #                         status_code=302, target_status_code=200)
