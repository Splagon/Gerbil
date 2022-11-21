import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django import forms


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


class RequestForm(forms.Form):
    availability = forms.DateField(required=True,
                                   widget=forms.SelectDateWidget(years=['2022', '2023']))
    number_of_lessons = forms.CharField(required=True,
                                        label="Number of lessons ", widget=forms.NumberInput)
    interval_between_lessons = forms.CharField(required=True,
                                               label="Time between lessons ", widget=forms.NumberInput)
    duration_of_lessons = forms.CharField(required=True,
                                          label="Lesson time", widget=forms.NumberInput)
    instruments = forms.CharField(required=False, label="Select the instrument you are interested in: ",
                                  widget=forms.Select(choices=[("", ""), ('violin', 'violin'), ('piano', 'piano'), ('cello', 'cello')]))
    teacher = forms.CharField(required=False,
                              label="Find a teacher that you know on this site", max_length=50)
