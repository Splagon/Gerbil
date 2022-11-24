from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .forms import SignUpForm, LogInForm, AdminSignUpForm
import operator


def home(request):
    return render(request, 'home.html')

def log_in(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #The line below should be changed when The
                #view that goes after the log in page is
                #implemented (see test_log_in_view.py line 57)
                #TLDR: change home for the name of said view
                return redirect("home")
    form =LogInForm()
    return render(request,'log_in.html',{"form": form})

def sign_up(request):
    if request.method == "POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html',{"form":form})

@login_required(login_url = "log_in")
def lessons(request):
    return render(request, 'lessons.html')

def admin_home(request):
    return render(request, 'admin/admin_home.html')

def admin_log_in(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #The line below should be changed when The
                #view that goes after the log in page is
                #implemented (see toperator.attrgetter('is_staff')est_log_in_view.py line 57)
                #TLDR: change home for the name of said view
                return redirect("admin_home")
    form =LogInForm()
    return render(request,'admin/admin_log_in.html',{"form": form})

@login_required(login_url = "log_in")
def admin_log_out(request):
    logout(request)
    return redirect("admin_home")

@user_passes_test(operator.attrgetter('is_superuser'), login_url = "admin_log_in")
def admin_sign_up(request):
    if request.method == "POST":
        form=AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_sign_up")
    else:
        form = AdminSignUpForm()
    return render(request, 'admin/admin_sign_up.html',{"form":form})

@user_passes_test(operator.attrgetter('is_staff'), login_url = "admin_log_in")
def admin_view_requests(request):
    return render(request, 'admin/admin_view_requests.html')

@user_passes_test(operator.attrgetter('is_superuser'), login_url = "admin_log_in")
def admin_view_users(request):
    return render(request, 'admin/admin_view_users.html')
