from django import forms
from .models import User

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name","last_name", "dateOfBirth"]
    
    # Not included in User model yet so comment these out for now
    #password = forms.CharField(label="Password", widget=forms.PasswordInput())
    #password_confirm = forms.CharField(label="Confirm password", widget=forms.PasswordInput())