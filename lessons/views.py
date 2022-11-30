from django.shortcuts import render, redirect
from .models import Request
from .forms import RequestForm
from .forms import LogInForm, UserForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .forms import SignUpForm, LogInForm, AdminSignUpForm
from django.contrib import messages
import datetime
import operator


def home(request):
    return render(request, 'home.html')

def requests(request):
    user = request.user
    requests = Request.objects.all().values()
    return render(request, 'requests.html', {'user': user, 'requests': requests})

# before going to request form, must make sure user is logged in
def request_form(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('requests')
    else:
        form = RequestForm()
    
    return render(request, 'request_form.html', {'form': form, })


def delete_request(request,id):
    request = Request.objects.get(id=id)
    request.delete()
    return redirect('requests')

def update_request(request,id):
    requestObject = Request.objects.get(id=id)
    form = RequestForm(request.POST or None, instance=requestObject)
    if form.is_valid():
        # TODO-- Refactor this asap
        availability_date = form.cleaned_data.get('availability_date')
        availability_time = form.cleaned_data.get('availability_time')
        duration_of_lessons = form.cleaned_data.get('duration_of_lessons')
        number_of_lessons = form.cleaned_data.get('number_of_lessons')
        interval_between_lessons = form.cleaned_data.get('interval_between_lessons')
        teacher = form.cleaned_data.get('teacher')
        instrument = form.cleaned_data.get('instrument')


        # Update the records after the user has made changes
        request = Request.objects.get(id=id)
        request.availability_date = availability_date
        request.availability_time = availability_time
        request.duration_of_lessons = duration_of_lessons
        request.number_of_lessons = number_of_lessons
        request.interval_between_lessons = interval_between_lessons
        request.teacher = teacher
        request.instrument = instrument


        request.save()
        return redirect('requests')
        
    return render(request, 'update_request_form.html', {'request': requestObject,'form' : form })
 

def log_in(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("lessons")
    form =LogInForm()
    return render(request,'log_in.html',{"form": form})

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
    user = request.user
    requests = Request.objects.all().values()
    return render(request, 'admin/admin_view_requests.html', {'user': user, 'requests': requests})

def admin_update_requests(request):
    requestObject = Request.objects.get(id=id)
    form = RequestForm(request.POST or None, instance=requestObject)
    if form.is_valid():
        # TODO-- Refactor this asap
        availability_date = form.cleaned_data.get('availability_date')
        availability_time = form.cleaned_data.get('availability_time')
        duration_of_lessons = form.cleaned_data.get('duration_of_lessons')
        number_of_lessons = form.cleaned_data.get('number_of_lessons')
        interval_between_lessons = form.cleaned_data.get('interval_between_lessons')
        teacher = form.cleaned_data.get('teacher')
        instrument = form.cleaned_data.get('instrument')

        # Update the records after the user has made changes
        request = Request.objects.get(id=id)
        request.availability_date = availability_date
        request.availability_time = availability_time
        request.duration_of_lessons = duration_of_lessons
        request.number_of_lessons = number_of_lessons
        request.interval_between_lessons = interval_between_lessons
        request.teacher = teacher
        request.instrument = instrument


        request.save()
        return redirect('admin_view_requests')
        
    return render(request, 'admin_update_request_form.html', {'request': requestObject,'form' : form })

@user_passes_test(operator.attrgetter('is_superuser'), login_url = "admin_log_in")
def admin_view_users(request):
    return render(request, 'admin/admin_view_users.html')

def profile(request):
    current_user = request.user
    print(request.user)
    if request.method == 'POST':
        form = UserForm(instance=current_user, data=request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, "Profile updated!")
            form.save()
            return redirect('lessons')
    else:
        form = UserForm(instance=current_user)
    return render(request, 'profile.html', {'form': form})
