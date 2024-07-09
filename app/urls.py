"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('search_results',views.search_results,name='search'),
    path('book',views.book,name='book'),
    # path('services',views.services,name='services'),
    path('achievements',views.achievements,name='achievements'),
    path('contact-us',views.contact_us,name='contact'),
    path('register',views.register,name='register'),
    path('login1',views.login1,name='login1'),
    path('logoutpage',views.logoutpage,name='logout'),
    path('logged',views.logged,name='logged'),
    path('signup',views.signup,name='signup'),
    path('form',views.contactinfo),
    path('payment',views.payment),
    path('gen_ticket',views.gen_ticket),
    path('ticket',views.ticket,name="ticket"),
    path('booki/', views.booki, name='booki'),
    path('cancel_ticket/<str:ref_no>/', views.cancel_ticket, name='cancel_ticket'),
    path('ticket_detail/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('download',views.download,name="download"),
    path('flight_list',views.flight_list,name="flight_list"),
    path('add_flight/', views.add_flight, name='add_flight'),
    path('delete_flight/<str:flight_id>/', views.delete_flight, name='delete_flight'),
    # path('cancel_ticket',views.cancel_ticket,name="cancel_ticket"),
    # Assuming you have a URL pattern like this in your urls.py 



]
