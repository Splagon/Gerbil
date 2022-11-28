from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
import datetime
INSTRUMENTS_TO_SELECT_FROM = [
    ('violin', 'violin'),
    ('double bass', 'double bass'),
    ('cello', 'cello'),
]

DURATIONS_TO_SELECT_FROM = [
    ('30', '30'),
    ('45', '45'),
    ('60', '60'),
]
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

class Request(models.Model):
    """Request from a student for a lesson"""
    availability_date = models.DateField( blank=False, default=datetime.date.today )
    availability_time = models.TimeField(blank=False, default="08:00")
    number_of_lessons = models.CharField(blank=False, max_length=3)
    interval_between_lessons = models.CharField(blank=False, max_length=3)
    duration_of_lessons = models.CharField(blank=False, max_length=4, choices=DURATIONS_TO_SELECT_FROM)
    instrument = models.CharField(blank=True, max_length=180, choices=INSTRUMENTS_TO_SELECT_FROM)
    teacher = models.CharField(blank=True,max_length=50)


    class Meta:
        """Model options."""
