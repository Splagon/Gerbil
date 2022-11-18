from django import forms
from django.core.validators import RegexValidator
from lessons.models import User

class LogInForm(forms.Form):
    username = forms.CharField(label = "Username")
    password = forms.CharField(label = "Password", widget= forms.PasswordInput())
