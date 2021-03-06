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
from typing import List, Any

from django.contrib import admin
from django.urls import path
from student import views

app_name = 'student'

urlpatterns = [
    path("", views.home, name='student home'),
    path("profile/", views.profile, name='profile'),
    path("edit/profile/", views.edit_profile, name='edit profile'),
    path("profile/visit/<int:id>", views.student_profile_visitor, name='profile visitor'),

]
