from django.test import TestCase
from lessons.models import SchoolBankAccount


class SchoolBankAccountTestCase(TestCase):
    def setUp(self):
        self.school_bank_account = User.objects.create_user(
            balance=0.0
        )

        
