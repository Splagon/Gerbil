import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django import forms
import datetime
INSTRUMENTS_TO_SELECT_FROM = [
    ('0', 'violin'),
    ('1', 'double bass'),
    ('2', 'cello'),
]

DURATIONS_TO_SELECT_FROM = [
    ('0', '30'),
    ('1', '60'),
    ('2', '90'),
    ('3', '120'),
]
class User(AbstractUser):
    username = models.EmailField(
        unique=True,
        blank=False,
        validators=[EmailValidator(
            message="Invalid email"
        )]
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
        null=True
    )


class Request(models.Model):
    """Request from a student for a lesson"""
    availability_date = models.DateTimeField( blank=False, default=datetime.date.today )
    availability_time = models.TimeField(blank=False, default="08:00")
    number_of_lessons = models.CharField(blank=False, max_length=3)
    interval_between_lessons = models.CharField(blank=False, max_length=3)
    duration_of_lessons = models.CharField(blank=False, max_length=1, choices=DURATIONS_TO_SELECT_FROM)
    instrument = models.CharField(blank=True, max_length=1, choices=INSTRUMENTS_TO_SELECT_FROM)
    teacher = models.CharField(blank=True,max_length=50)


    class Meta:
        """Model options."""