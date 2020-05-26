"""RTS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from faculty import views

app_name = 'faculty'

urlpatterns = [
    path("", views.home, name='faculty home'),
    path("faculty_profile/", views.profile, name='profile'),
    path("edit_profile/", views.edit_profile, name='edit profile'),
    path("faculty_availabilty/", views.availability_status, name='availability_status'),
    path("update_availabilty/", views.update_status, name='update_status'),

]
