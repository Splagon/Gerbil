"""msms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from lessons import views

urlpatterns = [
    path('', views.home, name='home'),
    path('requests/', views.requests, name='requests'),
    path('request-lesson/', views.request_form, name='request_form'),
    path('delete_request/<int:id>', views.delete_request, name='delete-request'),
    path('update_request/<int:id>', views.update_request, name='update-request'),

    path("log_in/", views.log_in, name="log_in"),
    path("log_out/", views.log_out, name="log_out"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("bookings/", views.view_bookings,name="view_bookings"),
    path("view_profile/", views.view_profile,name="view_profile"),
    path("bank_transfer/", views.bank_transfer, name= "bank_transfer"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('password/', views.password, name='password'),

    path('admin/', views.admin_home, name = 'admin_home'),
    path('admin/log_in/', views.admin_log_in, name = 'admin_log_in'),
    path('admin/log_out/', views.admin_log_out, name = 'admin_log_out'),
    path('admin/sign_up/', views.admin_sign_up, name = 'admin_sign_up'),
    path('admin/view_users/', admin.site.urls, name = 'admin_view_users'),
    path('admin/view_users/', views.admin_home, name = 'admin_view_users'),
    path('admin/view_requests/', views.admin_view_requests, name = 'admin_view_requests'),
    path('admin/update_request/<int:id>', views.update_request, name = 'admin_update_requests'),
    path('admin/delete_request/<int:id>', views.delete_request, name = 'admin_delete_requests'),
    path('admin/book_request/<int:id>', views.admin_book_request_form, name = 'admin_book_request_form'),


    path('profile/', views.profile, name='profile'),
    path('admin/view_bookings/', views.admin_view_bookings, name = 'admin_view_bookings'),
]
