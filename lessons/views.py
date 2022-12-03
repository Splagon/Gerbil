from django.shortcuts import render, redirect
from .models import User, Request, Term, BankTransfer, Invoice, SchoolBankAccount
from .forms import RequestForm
from .forms import LogInForm, UserForm, SignUpForm, PasswordForm, BankTransferForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from .forms import SignUpForm, LogInForm, AdminSignUpForm, TermForm
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .helpers import getDurationsToPrices
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
    return render(request, 'request_form.html', {'form': form})
    #return render(request, 'request_form.html', {'form': form, })



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
        totalPrice= int(form.cleaned_data.get('number_of_lessons')) * getDurationsToPrices(form.cleaned_data.get('duration_of_lessons'))

        old_request = Request.objects.get(id=id)
        old_price = old_request.totalPrice

        # Update the records after the user has made changes
        request = Request.objects.get(id=id)
        request.availability_date = availability_date
        request.availability_time = availability_time
        request.duration_of_lessons = duration_of_lessons
        request.number_of_lessons = number_of_lessons
        request.interval_between_lessons = interval_between_lessons
        request.teacher = teacher
        request.instrument = instrument
        request.totalPrice = totalPrice
        request.save()

        invoice_exists = Invoice.objects.filter(invoice_number =str(id)).exists()
        if(invoice_exists):
            update_invoice(id, str(old_price))

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

#@login_required
#def profile(request):

def create_invoice(id):
    request = Request.objects.get(id=id)
    amount = request.totalPrice
    user = request.username
    user.balance-= float(amount)
    user.save()

    invoice = Invoice.objects.create(
    unique_reference_number = str(request.requesterId)+"-"+str(request.id),
    invoice_number= str(request.id),
    student_id = request.requesterId,
    amount = float(request.totalPrice)
    )
    invoice.save()

def update_invoice(id, old_price):
    request = Request.objects.get(id=id)
    new_total = request.totalPrice

    user=request.username
    user.balance += float(old_price)
    user.balance -= float(new_total)
    user.save()

    invoice = Invoice.objects.get(invoice_number = str(id))
    invoice.amount= new_total
    invoice.save()



    #print(str(request.requesterId)+"-"+str(request.id))



def admin_book_request_form(request, id, requesterId):
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
        status = 'Booked'

        # Update the records after the user has made changes
        request = Request.objects.get(id=id)
        request.availability_date = availability_date
        request.availability_time = availability_time
        request.duration_of_lessons = duration_of_lessons
        request.number_of_lessons = number_of_lessons
        request.interval_between_lessons = interval_between_lessons
        request.teacher = teacher
        request.instrument = instrument
        request.status = status

        create_invoice(id)
        request.save()


        return redirect('admin_view_requests')
    return render(request, 'admin/admin_book_request_form.html', {'request': requestObject,'form' : form })

@login_required(login_url = "log_in")
def edit_profile(request):
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

@login_required(login_url = "log_in")
def bank_transfer(request):

    if request.method == 'POST':
        form = BankTransferForm(request.POST)
        if form.is_valid():

            exists = Invoice.objects.filter(invoice_number =form.cleaned_data.get('inv_number')).exists()
            print(exists)
            #15945615-7f29-4079-b567-a5a7ac6647a4
            if(exists == True):
                print("c1")


                amount = Request.objects.get(id=form.cleaned_data.get('inv_number'))

                requested = Request.objects.filter(id=form.cleaned_data.get('inv_number')).exists()
                print(requested)
                if(requested == True):
                    invoice = Invoice.objects.get(invoice_number =form.cleaned_data.get('inv_number'))
                    paid = invoice.paid
                    print(paid)
                    print("aa")

                    if(paid == False):

                        user = request.user
                        user.balance += float(amount.totalPrice)
                        invoice = Invoice.objects.get(invoice_number =form.cleaned_data.get('inv_number'))
                        invoice.paid = True
                        invoice.save()
                        user.save()
                        form.save(request.user,amount.totalPrice)

                        school_bank_account = SchoolBankAccount.objects.get(id=1)
                        school_bank_account.balance += float(amount.totalPrice)
                        school_bank_account.save()
                        print("succesful transfer")
                        return redirect('home')

                    else:
                        print("invoice has been paid already")
                        return render(request, 'bank_transfer.html', {'form': form})

                else:
                    form = BankTransferForm()

                    return render(request, 'bank_transfer.html', {'form': form})

            else:

                form = BankTransferForm()


                return render(request, 'bank_transfer.html', {'form': form})




        else:
            print("form wasnt valid")
            return redirect("home")
    else:

        form = BankTransferForm()
        return render(request, 'bank_transfer.html', {'form': form})

@login_required(login_url = "log_in")
def balance_and_transactions(request):
    user= request.user
    return render(request, "balance_and_transactions.html",{"user":user})

def admin_view_user_invoice(request,id):
    user = User.objects.get(id=id)
    user_invoices= Invoice.objects.filter(student_id=user.id)
    return render(request, "view_invoices.html",{"user":user,"user_invoices":user_invoices})

def admin_view_user_transfers(request,id):
    user = User.objects.get(id=id)
    user_transfers= BankTransfer.objects.filter(student_id=user.id)
    return render(request, "view_transfers.html",{"user":user,"user_transfers":user_transfers})


def view_invoices(request):
    user= request.user
    user_invoices= Invoice.objects.filter(student_id=user.id)
    return render(request, "view_invoices.html",{"user":user,"user_invoices":user_invoices})


def view_transfers(request):
    user= request.user
    user_transfers= BankTransfer.objects.filter(username=user.id)
    return render(request, "view_transfers.html",{"user":user,"user_transfers":user_transfers})

@login_required(login_url = "log_in")
def admin_view_school_balance_and_transfers(request):
    school_balance = SchoolBankAccount.objects.get(id=1)
    transfers = BankTransfer.objects.all().values()
    return render(request, 'admin/admin_view_school_balance_and_transfers.html', {'school_balance': school_balance, 'transfers': transfers})

@login_required(login_url = "log_in")
def admin_check_student_balance_and_transactions(request):
    users = User.objects.filter(is_superuser = False, is_staff = False)

    return render(request, "admin/admin_check_student_balance_and_transactions.html", {"users":users})



@login_required(login_url = "log_in")
def view_bookings(request):
    user = request.user
    requests = Request.objects.all().values()

    dates_of_lessons=[]

    for req in requests:
        dates = {}
        for i in range(int(req['number_of_lessons'])):
            if(req['status'] == "In Progress"):
                val = "n"
            else:
                val = "y"
            dates[val + str(req['id']) + str(i)] = req['availability_date'] + datetime.timedelta(weeks=(i * int(req['interval_between_lessons'])))
        dates_of_lessons.append(dates)
    print(dates_of_lessons)
    return render(request, 'bookings.html', {'user': user, 'requests': requests, 'arr': dates_of_lessons})

@user_passes_test(operator.attrgetter('is_staff'), login_url = "admin_log_in")
def admin_view_bookings(request):
    user = request.user
    requests = Request.objects.all().values()
    dates_of_lessons=[]

    for req in requests:
        dates = {}
        for i in range(int(req['number_of_lessons'])):
            if(req['status'] == "In Progress"):
                val = "n"
            else:
                val = "y"
            dates[val + str(req['id']) + str(i)] = req['availability_date'] + datetime.timedelta(weeks=(i * int(req['interval_between_lessons'])))
        dates_of_lessons.append(dates)
    print(dates_of_lessons)
    return render(request, 'admin/admin_bookings.html', {'user': user, 'requests': requests, 'arr': dates_of_lessons})

@user_passes_test(operator.attrgetter('is_staff'), login_url = "admin_log_in")
def admin_view_terms(request):
    terms = Term.objects.filter(endDate__gte = datetime.datetime.today()).values()
    return render(request, 'admin/admin_view_terms.html', {'terms': terms})

@user_passes_test(operator.attrgetter('is_staff'), login_url = "admin_log_in")
def admin_add_term(request):
    if request.method == 'POST':
        form = TermForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_view_terms')
    else:
        form = TermForm()

    return render(request, 'admin/admin_add_term.html', {'form': form})

@user_passes_test(operator.attrgetter('is_staff'), login_url = "admin_log_in")
def admin_edit_term(request,id):
    termInstance = Term.objects.get(id=id)
    form = TermForm(request.POST or None, instance=termInstance, idNum = id)
    if form.is_valid():
        # Update the records after the user has made changes
        term = Term.objects.get(id=id)
        term.startDate = form.cleaned_data.get('startDate')
        term.endDate = form.cleaned_data.get('endDate')
        term.save()
        return redirect('admin_view_terms')
    return render(request, 'admin/admin_edit_term.html', {'term': termInstance, 'form' : form })

@user_passes_test(operator.attrgetter('is_staff'), login_url = "admin_log_in")
def admin_delete_term(request,id):
    request = Term.objects.get(id=id)
    request.delete()
    return redirect('admin_view_terms')
