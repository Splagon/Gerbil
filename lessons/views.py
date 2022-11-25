from django.shortcuts import render, redirect
from .models import Request
from .forms import RequestForm
from .forms import LogInForm, UserForm, SignUpForm
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LogInForm
from django.contrib import messages



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
                return redirect("lessons")
    form =LogInForm()
    return render(request,'log_in.html',{"form": form})

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lessons")
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {"form": form})


def lessons(request):
    return render(request, 'lessons.html')


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
