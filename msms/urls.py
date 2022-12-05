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
    
    path('request_form_child/<str:name>', views.request_form_child, name='request_form_child'),
    
    path('add_child/', views.add_child, name='add_child'),
    path("view_child",views.view_child, name="view_child"),
    path("delete_child/<str:name>", views.delete_child, name="delete_child"),
    
    path('delete_request/<uuid:id>', views.delete_request, name='delete-request'),
    path('update_request/<uuid:id>', views.update_request, name='update-request'),
    path("admin/view_user_invoice/<int:id>", views.admin_view_user_invoice, name ="admin_view_user_invoice"),
    path("admin/view_user_transfers/<int:id>", views.admin_view_user_transfers,name= "admin_view_user_transfers"),

    path("log_in/", views.log_in, name="log_in"),
    path("log_out/", views.log_out, name="log_out"),
    path("sign_up/", views.sign_up, name="sign_up"),
    path("bookings/", views.view_bookings,name="view_bookings"),
    path("view_profile/", views.view_profile,name="view_profile"),
    path("bank_transfer/", views.bank_transfer, name= "bank_transfer"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('password/', views.password, name='password'),
    path("balance_and_transactions/", views.balance_and_transactions, name="balance_and_transactions"),
    path("view_invoices/", views.view_invoices, name="view_invoices"),
    path("view_transfers/",views.view_transfers,name="view_transfers"),


    path('admin/', views.admin_home, name = 'admin_home'),
    path("admin/check_student_balance_and_transactions/", views.admin_check_student_balance_and_transactions, name = "admin_check_student_balance_and_transactions"),
    path('admin/log_in/', views.admin_log_in, name = 'admin_log_in'),
    path('admin/log_out/', views.admin_log_out, name = 'admin_log_out'),
    path('admin/sign_up/', views.admin_sign_up, name = 'admin_sign_up'),

    path('admin/view_database/', admin.site.urls, name = 'admin_view_database'),
    path('admin/view_database/', views.admin_home, name = 'admin_view_database'),

    path('admin/view_requests/', views.admin_view_requests, name = 'admin_view_requests'),
    path('admin/view_bookings/', views.admin_view_bookings, name = 'admin_view_bookings'),

    path('admin/update_request/<uuid:id>', views.admin_update_requests, name = 'admin_update_requests'),

    path('admin/delete_request/<uuid:id>', views.admin_delete_request, name = 'admin_delete_requests'),
    path('admin/book_request/<uuid:id>/<int:requesterId>', views.admin_book_request_form, name = 'admin_book_request_form'),

    path('admin/view_terms/', views.admin_view_terms, name='admin_view_terms'),
    path('admin/add_term/', views.admin_add_term, name='admin_add_term'),
    path('admin/delete_term/<int:id>', views.admin_delete_term, name='admin_delete_term'),
    path('admin/edit_term/<int:id>', views.admin_edit_term, name='admin_edit_term'),
    path("admin_update_invoice/<uuid:id>/<str:old_price>", views.update_invoice, name="update_invoice"),

    path('admin/view_school_balance_and_transfers/', views.admin_view_school_balance_and_transfers, name= "admin_view_school_balance_and_transfers"),
    path('admin/create_invoice/<uuid:id>', views.create_invoice, name='admin_create_invoice')
]
