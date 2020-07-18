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
    path('all_available_faculty', views.all_available_faculty, name='all_available_faculty'),
    path('available_faculty', views.available_status_on_faculty, name='available_faculty'),
    path('not_avaialable_faculty', views.available_status_off_faculty, name='not_available_faculty'),
    path('search_availability_faculty', views.search_availability_faculty, name='search_availability_faculty'),
    path("faculty_profile/", views.profile, name='profile'),
    path("edit_profile/", views.edit_profile, name='edit profile'),
    path("faculty_availabilty/", views.availability_status, name='availability_status'),
    path("update_availabilty/", views.update_status, name='update_status'),
    path("schedule/", views.schedule_view, name='schedule_view'),
    path("schedule/today", views.today_schedule_view, name='schedule_view_today'),
    path("create_schedule/", views.schedule_create, name='create_schedule'),
    path("update_schedule/<int:id>/", views.schedule_update, name='update_schedule'),
    path("remove_schedule/<int:id>/", views.schedule_remove, name='remove_schedule'),
    path("schedule/chart/", views.schedule_chart_view, name='schedule_chart_view'),
    path('all_available_faculty_view', views.all_available_faculty_sidebar, name='all_available_faculty_sidebar'),
    path('available_faculty_view', views.available_status_on_faculty_sidebar, name='available_faculty_sidebar'),
    path('not_avaialable_faculty_view', views.available_status_off_faculty_sidebar, name='not_available_sidebar'),
    path('search_availability_faculty_view', views.search_availability_faculty_sidebar,
         name='search_availability_sidebar'),
    path('faculty/profile/<int:id>/', views.faculty_profile_visitor,
         name='faculty_profile'),
    path('schedule/chart/id/<int:id>/', views.schedule_chart_view_for_login_user,
         name='schedule_chart_view_for_login'),
    path('schedule/vistor/chart/id/<int:id>/', views.schedule_chart_view_for_visitors,
         name='schedule_chart_view_for_visitors'),

]
