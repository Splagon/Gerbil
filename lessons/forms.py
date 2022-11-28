from django import forms
from django.contrib.auth import get_user_model
from django.forms import widgets
from .models import User
from django.core.validators import RegexValidator

class LogInForm(forms.Form):
    username = forms.CharField(label = "Username")
    password = forms.CharField(label = "Password", widget= forms.PasswordInput())

class SignUpForm(forms.ModelForm):
    class Meta:
        #User
        model = get_user_model()
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


class PasswordForm(forms.Form):
    print("test")
    password = forms.CharField(
        label='Current password', widget=forms.PasswordInput())
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
        )]
    )
    password_confirmation = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation',
                        'Confirmation does not match password.')


class UserForm(forms.ModelForm):
    class Meta:
        """Form options."""

        model = User
        fields = ["username", "first_name", "last_name", "dateOfBirth"]
        widgets = {"dateOfBirth": widgets.DateInput(attrs={'type': 'date'})}
