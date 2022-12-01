from django.contrib import admin
from .models import User, Request

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users"""
    site_header = "MSMS Administration"
    list_display = [
        'username','first_name', 'last_name', 'is_active',
    ]

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = [
        'id','username', 'availability_date', 'number_of_lessons',
    ]
