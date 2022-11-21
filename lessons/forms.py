from django import forms

from django.forms import widgets
from .models import User
from django.core.validators import RegexValidator

class LogInForm(forms.Form):
    username = forms.CharField(label = "Username")
    password = forms.CharField(label = "Password", widget= forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name","last_name", "dateOfBirth"]
        widgets = {"dateOfBirth":widgets.DateInput(attrs={'type': 'date'})}
    password = forms.CharField(label="Password", 
                               widget=forms.PasswordInput(),
                               validators=[RegexValidator(
                                   regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$",
                                   message="Password must contain an uppercase character, a lowercase character, and a number"
                               )])
    password_confirm = forms.CharField(label="Confirm password", widget=forms.PasswordInput())
    
    def clean(self):
        super().clean()
        password = self.cleaned_data.get("password")
        pass_confirm = self.cleaned_data.get("password_confirm")
        if(password != pass_confirm):
            self.add_error("password_confirm", "Confirmation does not match password")
            
    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
                self.cleaned_data.get("username"),
                first_name = self.cleaned_data.get("first_name"),
                last_name = self.cleaned_data.get("last_name"),
                dateOfBirth = self.cleaned_data.get("dateOfBirth"),
                password = self.cleaned_data.get("password"),
            )
        return user
