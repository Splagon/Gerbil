from django.shortcuts import render, redirect
from .models import Request
from .forms import RequestForm

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