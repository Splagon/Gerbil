from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
import datetime
import uuid


from .helpers import getDurations, getInstruments,getIntervalBetweenLessons, getDurationsToPrices

class User(AbstractUser):
    username = models.EmailField(
        unique = True,
        blank = False,
        validators = [EmailValidator(
            message = "Invalid email"
        )],
        verbose_name = "email"
    )

    first_name = models.CharField(
        max_length=50,
        blank=False,
    )

    last_name = models.CharField(
        max_length=50,
        blank=False,
    )

    dateOfBirth = models.DateField(
        max_length=8,
        blank=True,
        null=True,
        verbose_name = "Date of Birth"
    )

    is_staff = models.BooleanField(verbose_name = "Admin Status")
    is_superuser = models.BooleanField(verbose_name = "Director Status")
    is_adult = models.BooleanField(verbose_name = "Adult Status", default=True)

    balance = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.username)


class Invoice(models.Model):
    """Invoice"""
    # requesterId - invoiceNumber
    unique_reference_number = models.CharField(blank=False,max_length= 100)
    # created automatically
    invoice_number=models.CharField(blank=False, max_length=36)
    # requesterId
    student_id =models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    # request.priceoflessons
    amount = models.FloatField(default=0.0)
    # default
    currently_paid = models.FloatField(default=0.0)


class BankTransfer(models.Model):
    invoice_number = models.CharField(blank=False, max_length=50)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    student_id=models.IntegerField(default=0)


class SchoolBankAccount(models.Model):
    balance= models.FloatField(default=0.0)




class Request(models.Model):
    """Request from a student for a lesson"""
    id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable = False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    availability_date = models.DateField( blank=False, default=now )
    availability_time = models.TimeField(blank=False, default="08:00")
    # number_of_lessons = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(20)])
    interval_between_lessons = models.CharField(blank=False, choices=getIntervalBetweenLessons(), max_length=2 )
    duration_of_lessons = models.CharField(blank=False, max_length=4, choices=getDurations())
    instrument = models.CharField(blank=True, max_length=180, choices=getInstruments())
    teacher = models.CharField(blank=True,max_length=50)
    status = models.CharField(max_length=50,default="In Progress", )
    totalPrice = models.CharField( max_length=50,default=0,  )
    requesterId = models.IntegerField(default=0)


    def __str__(self):
        return str(self.username)

    """ Find the """
    @property
    def lesson_dates(self):
        # Retrieve all term objects in ascending order
        terms = Term.objects.all().order_by('startDate').values()
        start_date = datetime.date.today()
        end_date = datetime.date.today()
        availability_date_new = datetime.date.fromisoformat(str(self.availability_date))
        if(len(terms) > 0):
            for i in range(len(terms)):
            # If the date falls mid-term:
                if(terms[i].get('startDate') < availability_date_new and availability_date_new < terms[i].get('endDate')):
                    start_date = self.availability_date
                    end_date = terms[i].get('endDate')

            # if the availability date falls in the break or between two terms
            for i in range(len(terms) - 1):
                if(terms[i].get('endDate') < availability_date_new and availability_date_new < terms[i+1].get('startDate')):
                    start_date = terms[i+1].get('startDate')
                    end_date = terms[i+1].get('endDate')

            # if the availabilty date is before the first term
            if(availability_date_new < terms[0].get('startDate')):
                start_date = terms[0].get('startDate')
                end_date = terms[0].get('endDate')

            # if the availability date is after the last term
            if(terms[len(terms)-1].get('endDate') <= availability_date_new):
                start_date = terms[len(terms)-1].get('endDate')
                end_date = terms[len(terms)-1].get('endDate')
        else:
            return {}
        # Finds the difference in weeks between two dates by finding the consecutive mondays
        startOfTerm = (start_date - datetime.timedelta(days=start_date.weekday()))
        endOfTerm = (end_date - datetime.timedelta(days=end_date.weekday()))
        numWeeks = (endOfTerm - startOfTerm).days / 7

        lesson_dates = {}
        for i in range(int(numWeeks)):
            lesson_date= start_date + datetime.timedelta(weeks=(i * int(self.interval_between_lessons)))
            lesson_dates[i] = lesson_date
        return lesson_dates
        
    @property
    def price_of_lessons(self):
        return float(len(self.lesson_dates)) * float(getDurationsToPrices(self.duration_of_lessons))

class Term(models.Model):
    termName = models.CharField(default="blank", max_length=50)
    startDate = models.DateField(blank = False, unique = True, default=datetime.date.today)
    endDate = models.DateField(blank = False, unique = True, default=datetime.date.today)

class Adult(User):
    class Meta:
        verbose_name = "Adult"
    # This class is a subclass of user, uses multi-table inheritance
    # An adult object will appear as a user and as an adult
    def __str__(self):
        return str(self.username)

class AdultChildRelationship(models.Model):
    # if adult deleted, all associated child relationships gone
    adult = models.ForeignKey(Adult, on_delete=models.CASCADE, blank=False, related_name = 'adult')
    # if child delete, all associated adults gone
    child = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name = 'child')
