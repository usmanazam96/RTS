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

from RTS.decorators import unauthenticated_user
from accounts import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    # password reset
    path('reset_password/',
         unauthenticated_user(auth_views.PasswordResetView.as_view(template_name="password_reset/password_reset.html")),
         name="reset_password"),

    path('reset_password_done/',
         unauthenticated_user(auth_views.PasswordResetDoneView.as_view(
             template_name="password_reset/password_reset_sent.html")),
         name="password_reset_done"),

    path('password_reset_confirm/<uidb64>/<token>/',
         unauthenticated_user(auth_views.PasswordResetConfirmView.as_view(
             template_name="password_reset/password_reset_form.html")),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         unauthenticated_user(auth_views.PasswordResetCompleteView.as_view(
             template_name="password_reset/password_reset_done.html")),
         name="password_reset_complete"),

]
