from django.shortcuts import render, redirect
from .models import Request, SchoolBankAccount, BankTransfer
from .forms import RequestForm
from .forms import LogInForm, UserForm, SignUpForm, PasswordForm, BankTransferForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .forms import SignUpForm, LogInForm, AdminSignUpForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.db.models import Q
import operator

def home(request):
    return render(request, 'home.html')


@login_required(login_url = "log_in")
def requests(request):
    user = request.user
    #requests = Request.objects.get(username = user.username).values()
    requests = Request.objects.filter(username=user).values()
    return render(request, 'requests.html', {'user': user, 'requests': requests})

@login_required(login_url = "log_in")
def request_form(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('requests')
    else:
        form = RequestForm()
    return render(request, 'request_form.html', {'form': form})

def log_in(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    form = LogInForm()
    return render(request, 'log_in.html', {"form": form})


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {"form": form})


@login_required(login_url = "log_in")
def view_profile(request):
    return render(request, 'view_profile.html')

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

@login_required(login_url = "log_in")
def log_out(request):
    logout(request)
    return redirect("home")

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

def admin_view_balance(request):
    school_bank_account = SchoolBankAccount.objects.get(id=1)
    transfers = BankTransfer.objects.values().all()
    return render(request, 'admin/admin_view_balance.html', {"school_bank_account": school_bank_account,"transfers": transfers})

@user_passes_test(operator.attrgetter('is_superuser'), login_url = "admin_log_in")
def admin_view_users(request):
    return render(request, 'admin/admin_view_users.html')

@login_required(login_url = "log_in")
def edit_profile(request):
    current_user = request.user
    print(request.user)
    if request.method == 'POST':
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('view_profile')
    else:
        form = UserForm(instance=current_user)
    return render(request, 'edit_profile.html', {'form': form})


@login_required(login_url = "log_in")
def password(request):
    current_user = request.user
    if request.method == 'POST':
        form = PasswordForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            if check_password(password, current_user.password):
                new_password = form.cleaned_data.get('new_password')
                current_user.set_password(new_password)
                current_user.save()
                login(request, current_user)
                messages.add_message(
                    request, messages.SUCCESS, "Password updated!")
                return redirect('view_profile')
    form = PasswordForm()
    return render(request, 'password.html', {'form': form})

@login_required(login_url = "log_in")
def bank_transfer(request):
    if request.method == 'POST':
        print("new pass")
        print(request.POST.get('new_password'))
        form = BankTransferForm(request.POST)
        if form.is_valid():
            form.save()
            print("form was _valid")


            return redirect('home')
            print("it was valid")
        else:
            print("form was not valid")
            return redirect("home")

    else:
        form = BankTransferForm()
        return render(request, 'bank_transfer.html', {'form': form})

@login_required(login_url = "log_in")
def view_bookings(request):
    user = request.user
    requests = Request.objects.all().values()
    #return render(request, 'requests.html', {'user': user, 'requests': requests})
    return render(request, "home.html")

@user_passes_test(operator.attrgetter('is_staff'), login_url = "admin_log_in")
def admin_view_bookings(request):
    user = request.user
    requests = Request.objects.all().values()
    #return render(request, 'requests.html', {'user': user, 'requests': requests})
    return render(request, "home.html")
