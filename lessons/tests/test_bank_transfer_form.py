"""Unit tests for the bank transfer form."""

from django import forms
from django.test import TestCase
from lessons.forms import BankTransferForm
from ..models import Invoice,User,BankTransfer

class BankTransferFormTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/default_invoice.json',
                'lessons/tests/fixtures/default_user2.json']


    def setUp(self):
        self.invoice = Invoice.objects.get(invoice_number="15945615-7f29-4079-b567-a5a7ac6647a4")
        self.form_input = {
        "inv_number":"15945615-7f29-4079-b567-a5a7ac6647a4",
        "paid_amount": 43.00
        }
        self.user = User.objects.get(username='michael.kolling@kcl.ac.uk')

    def test_valid_sign_up_form(self):
        form = BankTransferForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = BankTransferForm()
        self.assertIn('inv_number', form.fields)
        self.assertIn("paid_amount", form.fields)

    def test_entered_invoice_number_must_not_be_empty(self):
        self.form_input['inv_number'] = ''
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_entered_invoice_number_must_be_in_the_valid_format(self):
        self.form_input['inv_number'] = '15945615-7f29-4079-b567-a5a7ac6647a5'
        form = BankTransferForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_entered_amount_can_be_an_int(self):
        self.form_input['paid_amount'] = 43
        form = BankTransferForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_entered_amount_can_be_a_float(self):
        self.form_input['paid_amount'] = 43.00
        form = BankTransferForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_entered_invoice_number_must_be_valid(self):
        self.form_input['inv_number'] = '15945615-7a5'
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_entered_invoice_number_must_contain_dashes(self):
        self.form_input['inv_number'] = '159456157f294079b567a5a7ac6647a5'
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_entered_invoice_number_cannot_be_blank(self):
        self.form_input['inv_number'] = ''
        form = BankTransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    def test_bank_transfer_form_must_save_correctly(self):
        form=BankTransferForm(data=self.form_input)
        before_count = BankTransfer.objects.count()
        form.save(self.user)
        after_count = BankTransfer.objects.count()
        self.assertEqual(after_count, before_count+1)
        bank_transfer = BankTransfer.objects.get(invoice_number=self.form_input['inv_number'])
        self.assertEqual(bank_transfer.invoice_number, self.form_input['inv_number'])
        self.assertEqual(bank_transfer.username, self.user)
        self.assertEqual(bank_transfer.amount, self.form_input['paid_amount'])
        self.assertEqual(bank_transfer.student_id,self.user.id)
