from django.shortcuts import render, redirect
from .forms import LogInForm, UserForm, SignUpForm
from django.contrib.auth import authenticate, login
from .forms import SignUpForm
from .forms import LogInForm
from django.contrib import messages


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
                # The line below should be changed when The
                # view that goes after the log in page is
                # implemented (see test_log_in_view.py line 57)
                # TLDR: change home for the name of said view
                return redirect("lessons")
    form = LogInForm()
    return render(request, 'log_in.html', {"form": form})


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
