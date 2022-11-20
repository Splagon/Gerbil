from django.shortcuts import render, redirect
from .forms import SignUpForm

def home(request):
    return render(request, 'home.html')

def sign_up(request):
    if request.method == "POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lessons")
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html',{"form":form})

def lessons(request):
    return render(request, 'lessons.html')
