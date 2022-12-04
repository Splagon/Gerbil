from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.utils.timezone import now
import datetime
import uuid
from .helpers import getDurations, getInstruments, getStatuses

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
    is_adult = models.BooleanField(verbose_name = "Adult Status", default=False)
    
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return self.username


class Invoice(models.Model):
    """Invoice"""
    unique_reference_number = models.CharField(blank=False,max_length= 35)
    invoice_number=models.CharField(blank=False, max_length=50)
    student_id =models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    amount = models.FloatField(default=0.0)





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
    number_of_lessons = models.CharField(blank=False, max_length=3)
    interval_between_lessons = models.CharField(blank=False, max_length=3)
    duration_of_lessons = models.CharField(blank=False, max_length=4, choices=getDurations())
    instrument = models.CharField(blank=True, max_length=180, choices=getInstruments())
    teacher = models.CharField(blank=True,max_length=50)
    status = models.CharField(max_length=50,default="In Progress", )
    totalPrice = models.CharField( max_length=50,default=0,  )
    requesterId = models.IntegerField(default=0)

class Term(models.Model):
    startDate = models.DateField(blank = False, unique = True, default=datetime.date.today)
    endDate = models.DateField(blank = False, unique = True, default=datetime.date.today)

class Adult(User):
    # This class is a subclass of user, uses multi-table inheritance
    # An adult object will appear as a user and as an adult
    def __str__(self):
        return self.username

class AdultChildRelationship(models.Model):
    # if adult deleted, all associated child relationships gone
    adult = models.ForeignKey(Adult, on_delete=models.CASCADE, blank=False)
    # if child delete, all associated adults gone
    child = models.CharField(max_length=50,blank=False)
    