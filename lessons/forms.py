from django import forms
from .models import Request
from django.contrib.auth import get_user_model
from django.forms import widgets
from .models import User, Invoice
from django.core.validators import RegexValidator
import datetime

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["invoice_number"]
        widgets = {}

    def clean(self):
        super().clean()
        entire_reference_number = self.cleaned_data.get("invoice_number")
        if("-" not in entire_reference_number):
            self.add_error("invoice_number","invoice number is missing a separator")

        else:

            reference_number = self.cleaned_data.get("invoice_number").split("-")[0]
            invoice_number = self.cleaned_data.get("invoice_number").split("-")[1]

            if(reference_number.isdigit()== False):
                self.add_error("invoice_number", "reference number is invalid")

            if(invoice_number.isdigit()== False):
                self.add_error("invoice_number", "invoice number is invalid")




    def save(self):
        super().save(commit=False)
        invoice = Invoice.objects.create(
        reference_number = self.cleaned_data.get("invoice_number").split("-")[0],
        invoice_number = self.cleaned_data.get("invoice_number").split("-")[1]

        )
        return invoice

class RequestForm(forms.ModelForm):
    """Form enabling students to make lesson requests."""

    class Meta:
        model = Request
        fields = ['availability_date','availability_time', 'number_of_lessons','interval_between_lessons', 'duration_of_lessons', 'instrument', 'teacher']
        widgets = {
            'availability_date' : forms.DateTimeInput(attrs={'type' : 'date', 'min': datetime.date.today() } ),
            'availability_time' : forms.TimeInput(attrs={'type' : 'time', 'min': '08:00', 'max': '17:30'}),
            'instrument' : forms.Select(),
            'interval_between_lessons' : forms.NumberInput(),
            'number_of_lessons' : forms.NumberInput(),
            'duration_of_lessons' : forms.Select(),
        }
    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()

    def save(self):
        """Create a new request."""
        super().save(commit=False)
        request = Request.objects.create(
            availability_date=self.cleaned_data.get('availability_date'),
            availability_time=self.cleaned_data.get('availability_time'),
            number_of_lessons=self.cleaned_data.get('number_of_lessons'),
            interval_between_lessons = self.cleaned_data.get('interval_between_lessons'),
            duration_of_lessons=self.cleaned_data.get('duration_of_lessons'),
            instrument=self.cleaned_data.get('instrument'),
            teacher=self.cleaned_data.get('teacher'),
        )

        return request





class LogInForm(forms.Form):
    username = forms.CharField(label = "Username")
    password = forms.CharField(label = "Password", widget= forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
        #User
        model = get_user_model()
        fields = ["username", "first_name","last_name", "dateOfBirth"]
        widgets = {"dateOfBirth":widgets.DateInput(attrs={'type': 'date'})}
    password = forms.CharField(label="Password",
                            widget=forms.PasswordInput(),
                            validators=[RegexValidator(
                                regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$",
                                message="Password must contain an uppercase character, a lowercase character, and a number"
                            )])
    password_confirm = forms.CharField(label="Confirm password", widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        password = self.cleaned_data.get("password")
        pass_confirm = self.cleaned_data.get("password_confirm")
        if(password != pass_confirm):
            self.add_error("password_confirm", "Confirmation does not match password")

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
                self.cleaned_data.get("username"),
                first_name = self.cleaned_data.get("first_name"),
                last_name = self.cleaned_data.get("last_name"),
                dateOfBirth = self.cleaned_data.get("dateOfBirth"),
                password = self.cleaned_data.get("password"),
        )
        return user

class AdminSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "dateOfBirth", "is_superuser"]
        widgets = {"dateOfBirth":widgets.DateInput(attrs={'type': 'date'}),
                   "is_superuser":widgets.CheckboxInput
        }

    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput(),
                               validators=[RegexValidator(
                                   regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$",
                                   message="Password must contain an uppercase character, a lowercase character, and a number"
                               )])
    password_confirm = forms.CharField(label="Confirm password", widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        password = self.cleaned_data.get("password")
        pass_confirm = self.cleaned_data.get("password_confirm")
        if(password != pass_confirm):
            self.add_error("password_confirm", "Confirmation does not match password")

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
                self.cleaned_data.get("username"),
                first_name = self.cleaned_data.get("first_name"),
                last_name = self.cleaned_data.get("last_name"),
                dateOfBirth = self.cleaned_data.get("dateOfBirth"),
                password = self.cleaned_data.get("password"),
                is_staff = True,
                is_superuser = self.cleaned_data.get("is_superuser")
            )
        return user

class UserForm(forms.ModelForm):
    class Meta:
        """Form options."""

        model = User
        fields = ["username", "first_name", "last_name", "dateOfBirth"]
        widgets = {"dateOfBirth": widgets.DateInput(attrs={'type': 'date'})}
