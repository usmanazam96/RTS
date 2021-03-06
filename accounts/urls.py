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
from accounts import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path("", views.home, name='home'),
    path('login/', views.loginPage, name="login"),
    path('login_role_select/', views.login_role_select, name="login_role_select"),
    path('logout/', views.logoutUser, name="logout"),
    path('create_faculty/', views.createFaculty, name="create_faculty"),
    path('create_student/', views.createStudent, name="create_student"),
    path('create_admin/', views.createAdmin, name="create_admin"),
    path('faculty/', views.faculty_list_view, name="faculty_list"),
    path('students/', views.student_list_view, name="students_list"),
    path('admins/', views.admin_list_view, name="admins_list"),
    path('users/', views.user_list_view, name="users_list"),
    path('un_active_users/', views.un_active_user_list_view, name="un_active_users_list"),
    path('active_users/', views.active_user_list_view, name="active_users_list"),
    path('change_password/', views.change_password, name="change_password"),
    path('create_student_with_existing_user/<int:id>/', views.createStudentWithExistingUser,
         name="create_student_with_existing_user"),
    path('create_admin_with_existing_user/<int:id>/', views.createAdminWithExistingUser,
         name="create_admin_with_existing_user"),
    path('create_faculty_with_existing_user/<int:id>/', views.createFacultyWithExistingUser,
         name="create_faculty_with_existing_user"),
    path('active_user/<int:id>/', views.active_user, name="active_user"),
    path('un_active_user/<int:id>/', views.un_active_user, name="un_active_user"),
    path('edit_user/<int:id>/', views.edit_user, name="edit_user"),
    path('edit_student/<int:id>/', views.edit_student, name="edit_student"),
    path('edit_faculty/<int:id>/', views.edit_faculty, name="edit_faculty"),
    path('edit_admin/<int:id>/', views.edit_admin, name="edit_admin"),
    path('remove_admin_group/<int:id>/', views.remove_admin_group, name="remove_admin_group"),
    path('remove_faculty_group/<int:id>/', views.remove_faculty_group, name="remove_faculty_group"),
    path('remove_student_group/<int:id>/', views.remove_student_group, name="remove_student_group"),
    path('faculty_profile/<int:id>/', views.faculty_profile, name="faculty_profile"),
    path('faculty_profile_visitor/<int:id>/', views.faculty_profile_visitor, name="faculty_profile_visitor"),
    path('student_profile/<int:id>/', views.student_profile, name="student_profile"),


]
