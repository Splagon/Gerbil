from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now
import datetime
import uuid
from .helpers import getDurations, getInstruments, getStatuses

allUsers = []

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

    balance = models.FloatField(default=0.0)

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        allUsers.append(self)
        # print(allUsers)
    
    def __str__(self):
        return self.username


class Invoice(models.Model):
    """Invoice"""
    unique_reference_number = models.CharField(blank=False,max_length= 100)
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
    number_of_lessons = models.IntegerField(blank=False, validators=[MinValueValidator(0), MaxValueValidator(20)])
    interval_between_lessons = models.IntegerField(blank=False, validators=[MinValueValidator(0)])
    duration_of_lessons = models.CharField(blank=False, max_length=4, choices=getDurations())
    instrument = models.CharField(blank=True, max_length=180, choices=getInstruments())
    teacher = models.CharField(blank=True,max_length=50)
    status = models.CharField(max_length=50,default="In Progress", )
    totalPrice = models.CharField( max_length=50,default=0,  )
    requesterId = models.IntegerField(default=0)

    def __str__(self):
        return self.username
        
    @property
    def lesson_dates(self):
        lesson_dates=[]
        for i in range(int(self.number_of_lessons)):
            lesson_date = self.availability_date + datetime.timedelta(weeks=(i * int(self.interval_between_lessons)))
            lesson_dates.append(lesson_date)
        return lesson_dates

class Term(models.Model):
    termName = models.CharField(default="blank", max_length=50)
    startDate = models.DateField(blank = False, unique = True, default=datetime.date.today)
    endDate = models.DateField(blank = False, unique = True, default=datetime.date.today)
