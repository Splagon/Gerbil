from django.shortcuts import render
from .models import RequestForm


def home(request):
    return render(request, 'home.html')


def request_form(request):
    form = RequestForm()
    return render(request, 'request_form.html', {'form': form})
