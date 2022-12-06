from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
import datetime
import uuid
from .helpers import getDurations, getInstruments, getIntervalBetweenLessons

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
    child_name = models.CharField(blank=False, verbose_name = "Student's name", max_length=50, default = "")
    is_staff = models.BooleanField(verbose_name = "Admin Status")
    is_superuser = models.BooleanField(verbose_name = "Director Status")
    number_of_students = models.PositiveIntegerField(
        verbose_name = "Number of children / students",
        validators = [MinValueValidator(1), MaxValueValidator(20)],
        default=1
    )

    child_age = models.IntegerField(blank=False, verbose_name = "Student's age", default = 15, validators=[MinValueValidator(5), MaxValueValidator(80)])

    balance = models.FloatField(default=0.0)

    def __str__(self):
        return self.username


class Invoice(models.Model):
    """Invoice"""
    unique_reference_number = models.CharField(blank=False,max_length= 100)
    invoice_number=models.CharField(blank=False, max_length=36)
    student_id =models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    amount = models.FloatField(default=0.0)
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
    student = models.CharField(verbose_name = "Register a student", max_length=50) # want to add a choices field for each child
    status = models.CharField(max_length=50,default="In Progress", )
    totalPrice = models.CharField( max_length=50,default=0,  )
    requesterId = models.IntegerField(default=0)

    def __str__(self):
        return self.username
    
    # @property
    # def student_info(self):
    #     print(self.username)

    @property
    def lesson_dates(self):

        terms = Term.objects.filter(
        endDate__gte=datetime.datetime.today()).values()

        if(len(terms) > 0):
            end_of_term_date = terms.first()['endDate']
        else:
            end_of_term_date = datetime.date.today()
        # Finds the difference in weeks between two dates by finding the consecutive mondays
        startOfTerm = (self.availability_date - datetime.timedelta(days=self.availability_date.weekday()))
        endOfTerm = (end_of_term_date - datetime.timedelta(days=end_of_term_date.weekday()))
        numWeeks = (endOfTerm - startOfTerm).days / 7

        lesson_dates = {}
        for i in range(int(numWeeks)):
            lesson_date= self.availability_date + datetime.timedelta(weeks=(i * int(self.interval_between_lessons)))
            lesson_dates[i] = lesson_date
        return lesson_dates



class Term(models.Model):
    startDate = models.DateField(blank = False, unique = True, default=datetime.date.today)
    endDate = models.DateField(blank = False, unique = True, default=datetime.date.today)

# class Adult(User):
#     class Meta:
#         verbose_name = "Adult"
#     # This class is a subclass of user, uses multi-table inheritance
#     # An adult object will appear as a user and as an adult
#     def __str__(self):
#         return self.username

# class AdultChildRelationship(models.Model):
#     # if adult deleted, all associated child relationships gone
#     adult = models.ForeignKey(Adult, on_delete=models.CASCADE, blank=False)
#     # if child delete, all associated adults gone
#     child = models.CharField(max_length=50,blank=False)
    