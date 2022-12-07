from django.contrib import admin
from .models import User, Request, Term, Invoice,BankTransfer, SchoolBankAccount, Adult, AdultChildRelationship

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""
    site_header = "MSMS Administration"
    list_display = [
        'username','first_name', 'last_name', 'is_active', 'is_adult'
    ]

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    #'number_of_lessons'
    list_display = [
        'id','username', 'availability_date',
    ]


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = [
        'id','startDate', 'endDate',
    ]

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display=[
    "invoice_number","student_id", "unique_reference_number"
    ]

@admin.register(BankTransfer)
class BankTransferAdmin(admin.ModelAdmin):
    list_display=[

    "invoice_number","amount"
    ]

@admin.register(SchoolBankAccount)
class SchoolBankAccountAdmin(admin.ModelAdmin):
    list_display=["balance"]

@admin.register(Adult)
class AdultAdmin(admin.ModelAdmin):
    list_display = [
        'username','first_name', 'last_name', 'is_active', 'is_adult'
    ]

@admin.register(AdultChildRelationship)
class AdultChildRelationAdmin(admin.ModelAdmin):
    list_display = [
        "adult", "child"
    ]
