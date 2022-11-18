from django.contrib.auth import authenticate, login
from django.shortcuts import redirect,render
from .forms import LogInForm

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

def home(request):
    return render(request, 'home.html')
