from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
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


class Invoice(models.Model):
    """Invoice"""
    reference_number = models.CharField(blank=False ,max_length = 12)
    invoice_number = models.CharField(blank=False,max_length = 12)


class Request(models.Model):
    """Request from a student for a lesson"""
    id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable = False)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    availability_date = models.DateTimeField( blank=False, default=datetime.date.today, )
    availability_time = models.TimeField(blank=False, default="08:00")
    number_of_lessons = models.CharField(blank=False, max_length=3)
    interval_between_lessons = models.CharField(blank=False, max_length=3)
    duration_of_lessons = models.CharField(blank=False, max_length=4, choices=getDurations())
    instrument = models.CharField(blank=True, max_length=180, choices=getInstruments())
    teacher = models.CharField(blank=True,max_length=50)
    status = models.CharField(max_length=50,default="In Progress", )
    totalPrice = models.CharField( max_length=50,default=0,  )



    class Meta:
        """Model options."""
