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
    path('contact',views.contact,name='contact'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('form',views.contactinfo),
    path('payment',views.payment),
    path('contact-us',views.contact_us,name='contact'),
    path('gen_ticket',views.gen_ticket),
    path('ticket',views.ticket,name="ticket")


]
