from django import forms
from .models import Request ,Term
from django.contrib.auth import get_user_model, authenticate
from django.forms import widgets

from .models import User, BankTransfer, Adult, AdultChildRelationship
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
# from .helpers import getDurationsToPrices

from django.db.models import Q
import datetime


class BankTransferForm(forms.ModelForm):
    class Meta:
        model = BankTransfer
        fields =[]

    inv_number = forms.CharField(
    label='Enter invoice number:',
    widget=forms.TextInput(),
    validators=[RegexValidator(
    regex=r'^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$',

    #regex=r'^[0-9]+-[0-9]+',

            message='Invoice  format is not valid'
            )]
            )
    paid_amount = forms.FloatField(min_value=0.01, max_value=9999.99,
    label="Enter amount to pay",
    widget= forms.NumberInput(attrs={
                'max': '9999.9',
                'min': '0.01',
            }),validators=[MinValueValidator(0.01), MaxValueValidator(9999.99)])





    def clean(self):
        super().clean()

    def save(self,user):
        super().save(commit=False)

        bank_transfer = BankTransfer.objects.create(
        invoice_number= self.cleaned_data.get("inv_number"),
        username=user,
        amount=self.cleaned_data.get("paid_amount"),
        student_id= user.id
        )

        return bank_transfer


class RequestForm(forms.ModelForm):
    """Form enabling students to make lesson requests."""

    class Meta:
        labels = {
            'availability_date' : 'Please select a date for your first lesson',
            'availability_time' : 'Please select a time to start your lesson. Note that it can\'t start before 8:00 or after 17:30',
            'instrument' : 'Please select the instrument you\'d like to start having lessons in',
            'interval_between_lessons' : 'Interval between lessons(in weeks)',
            'teacher' : 'Please select a preferred teacher',
        }
        model = Request

        fields = ['availability_date','availability_time','interval_between_lessons', 'duration_of_lessons', 'instrument', 'teacher']
        widgets = {
            'availability_date' : widgets.DateInput(format='%Y-%m-%d', attrs={'type' : 'date'}, ),
            'availability_time' : widgets.TimeInput(attrs={'type' : 'time', 'min': '08:00', 'max': '17:30'}),
            'instrument' : widgets.Select(),
            'interval_between_lessons' : widgets.Select(),
            # 'number_of_lessons' : widgets.NumberInput(),
            'duration_of_lessons' : widgets.Select(),
        }

    def clean(self):
        """Clean the data and generate messages for any errors."""        
        availability_time = self.cleaned_data['availability_time']
        if availability_time < datetime.time(hour=8, minute=0, second=0):
            raise forms.ValidationError('Time cannot be before 8.')

        elif availability_time > datetime.time(hour=17, minute=30, second=0):
            raise forms.ValidationError('Time cannot be after 17:30.')


        super().clean()

    # Saves a new request form
    def save(self, user):
        """Create a new request."""

        super().save(commit=False)
        request = Request.objects.create(
            username = user,
            availability_date=self.cleaned_data.get('availability_date'),
            availability_time=self.cleaned_data.get('availability_time'),
            interval_between_lessons = self.cleaned_data.get('interval_between_lessons'),
            duration_of_lessons=self.cleaned_data.get('duration_of_lessons'),
            instrument=self.cleaned_data.get('instrument'),
            teacher=self.cleaned_data.get('teacher'),
            status = 'In Progress',
            requesterId= user.id

        )


        return request
        
class LogInForm(forms.Form):
    username = forms.CharField(label = "Username")
    password = forms.CharField(label = "Password", widget= forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
        #User
        model = get_user_model()
        fields = ["username", "first_name","last_name", "dateOfBirth", "is_adult"]
        widgets = {"dateOfBirth":widgets.DateInput(attrs={'type': 'date'}),
                   "is_adult":widgets.CheckboxInput}
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
        is_adult = self.cleaned_data.get("is_adult")
        if(is_adult):
            user = Adult.objects.create_user(
                self.cleaned_data.get("username"),
                first_name = self.cleaned_data.get("first_name"),
                last_name = self.cleaned_data.get("last_name"),
                dateOfBirth = self.cleaned_data.get("dateOfBirth"),
                password = self.cleaned_data.get("password"),
                is_adult = self.cleaned_data.get("is_adult")
            )
        else:
            user = User.objects.create_user(
                    self.cleaned_data.get("username"),
                    first_name = self.cleaned_data.get("first_name"),
                    last_name = self.cleaned_data.get("last_name"),
                    dateOfBirth = self.cleaned_data.get("dateOfBirth"),
                    password = self.cleaned_data.get("password"),
                    is_adult = self.cleaned_data.get("is_adult")
            )
        return user

class PasswordForm(forms.Form):
    password = forms.CharField(
        label='Current password', widget=forms.PasswordInput())
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
        )]
    )
    password_confirmation = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation',
                        'Confirmation does not match password.')

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


class TermForm(forms.ModelForm):
    """Form enabling students to make lesson requests."""
    def __init__(self, *args, **kwargs):
        self.idNum = kwargs.pop('idNum', None)
        super(TermForm,self).__init__(*args, **kwargs)

    class Meta:
        labels = {
            'startDate' : 'Please select the start date for the term',
            'endDate' : 'Please select the start date for the term',
        }
        model = Term
        fields = ['startDate','endDate']
        widgets = {
            'startDate' : forms.DateInput(format='%d/%m/%Y', attrs={'type' : 'date'}, ),
            'endDate'   : forms.DateInput(format='%d/%m/%Y', attrs={'type' : 'date'}, )
        }

    def clean(self):
        """Clean the data and generate messages for any errors."""

        currStartDate = self.cleaned_data['startDate']
        currEndDate = self.cleaned_data['endDate']

        isValidationError = False
        errorMessage = ""
        if(currEndDate < currStartDate):
            errorMessage = 'End date cannot be before start date'
            self.add_error('endDate', errorMessage)
            isValidationError = True

        errorMessage = 'Date cannot be more than 2 years in the past.'
        if(currStartDate <= datetime.date.today() - datetime.timedelta(days=365*2)):
            self.add_error('startDate', errorMessage)
            isValidationError = True

        if(currEndDate <= datetime.date.today() - datetime.timedelta(days=365*2)):
            self.add_error('endDate', errorMessage)
            isValidationError = True

        currentTerms = list(Term.objects.exclude(id=self.idNum).values())
        overlappingTerms = []
        for term in currentTerms:
            startDate = term.get('startDate')
            endDate = term.get('endDate')
            if (not((currEndDate < startDate and currStartDate < startDate) or (currEndDate > endDate and currStartDate > endDate))):
                overlappingTerms.append(term)

        if (len(overlappingTerms) > 0):
            errorMessage = 'Term dates overlap with a term from ' + str(overlappingTerms[0].get('startDate')) + ' to '  + str(overlappingTerms[0].get('endDate'))
            self.add_error('startDate', errorMessage)
            self.add_error('endDate', errorMessage)
            isValidationError = True

        if (isValidationError):
            raise forms.ValidationError(errorMessage)

        super().clean()


    def save(self):
        """Create a new request."""
        super().save(commit=False)
        term = Term.objects.create(
            startDate = self.cleaned_data['startDate'],
            endDate = self.cleaned_data['endDate']
        )
        return term

class AdultChildRelationForm(forms.ModelForm):
    class Meta:
        model = AdultChildRelationship
        fields=["adult", "child"]

    def clean(self):
        super().clean()
        the_adult = self.cleaned_data.get("adult")
        the_child = self.cleaned_data.get("child")
        if the_adult == None:
            self.add_error("adult","No adult assigned (this should not be possible)")
        else:
            if the_adult == the_child:
                self.add_error("child","Cannot add yourself as a child.")
            else:
                if User.objects.filter(username=the_child).exists():
                    if AdultChildRelationship.objects.filter(adult=the_adult, child=the_child).exists():
                        self.add_error("child", "This relationship already exists")
                    else:
                        pass
                else:
                    self.add_error("child","Child email has invalid format or does not correspond with any existing user in our database.")


    def save(self):
        super().save(commit=False)
        rel = AdultChildRelationship.objects.create(
            adult = self.cleaned_data.get("adult"),
            child = self.cleaned_data.get("child")
        )
        return rel
