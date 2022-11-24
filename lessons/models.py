from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator


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
        max_length = 50,
        blank = False,
    )

    last_name = models.CharField(
        max_length = 50,
        blank = False,
    )

    dateOfBirth = models.DateField(
        max_length = 10,
        blank = True,
        null = True,
        verbose_name = "Date of Birth"
    )

    is_staff = models.BooleanField(verbose_name = "Admin Status")
    is_superuser = models.BooleanField(verbose_name = "Director Status")
