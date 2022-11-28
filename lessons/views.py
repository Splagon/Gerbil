from django.shortcuts import render, redirect
from .forms import LogInForm, UserForm, SignUpForm, PasswordForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password



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


@login_required
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


@login_required
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
                return redirect('lessons')
    form = PasswordForm()
    return render(request, 'password.html', {'form': form})
