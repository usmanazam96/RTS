from django.contrib import messages
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect

# Create your views here.
from RTS.decorators import unauthenticated_user

from faculty.models import *

from accounts.forms import *


def home(request):
    return render(request, 'accounts/home.html')


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.error(request, 'Invalid User or password')
    context = {'title': 'accounts | login'}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('accounts:login')


# admin

def createAdmin(request):
    if request.method == "GET":
        user_form = UserForm()
        faculty_form = AdminForm()
        context = dict(page_title='Admin-Create Faculty', h1_title='New Admin Account', url='createfaculty',
                       card_title="Account Information", user_form=user_form, form=faculty_form)
        return render(request, 'accounts/admin_create_form.html', context)
    else:
        registered = False
        user_form = UserForm(data=request.POST)
        admin_form = AdminForm(data=request.POST)
        if user_form.is_valid() and admin_form.is_valid():
            user: User = user_form.save()
            user.set_password(user.password)
            user.save()
            admin: Admin = admin_form.save(commit=False)
            admin.user = user
            if 'profile_pic' in request.FILES:
                admin.profile_pic = request.FILES['profile_pic']
            admin.save()
            group = Group.objects.get(name='admin')
            user.groups.add(group)
            registered = True
        if registered:
            messages.success(request, 'Account created  Successfully')
            return redirect('accounts:admin_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Create admin', h1_title='New admin Account', url='createadmin',
                           card_title="Account Information", user_form=user_form, form=admin_form)
            return render(request, 'accounts/admin_create_form.html', context)


def admin_list_view(request):
    admin_list = Admin.objects.all()
    context = dict(page_title='Accounts-Admins', h1_title='Admins', url='Admins',
                   card_title="All Admins", admin_list=admin_list)
    return render(request, 'accounts/admin_list.html', context)


# faculty


def createFaculty(request):
    if request.method == "GET":
        user_form = UserForm()
        faculty_form = FacultyForm()
        context = dict(page_title='Accounts-Create Faculty', h1_title='New Faculty Account', url='createfaculty',
                       card_title="Account Information", user_form=user_form, form=faculty_form)
        return render(request, 'accounts/faculty_create_form.html', context)
    else:
        registered = False
        user_form = UserForm(data=request.POST)
        faculty_form = FacultyForm(data=request.POST)
        if user_form.is_valid() and faculty_form.is_valid():
            user: User = user_form.save()
            user.set_password(user.password)
            user.save()
            faculty: Faculty = faculty_form.save(commit=False)
            faculty.user = user
            if 'profile_pic' in request.FILES:
                faculty.profile_pic = request.FILES['profile_pic']
            faculty.save()
            faculty_availability = FacultyAvailability(faculty=faculty)
            faculty_availability.save()
            group = Group.objects.get(name='faculty')
            user.groups.add(group)
            registered = True
        if registered:
            messages.success(request, 'Account created  Successfully')
            return redirect('accounts:faculty_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Create Faculty', h1_title='New Faculty Account', url='createfaculty',
                           card_title="Account Information", user_form=user_form, form=faculty_form)
            return render(request, 'accounts/faculty_create_form.html', context)


def faculty_list_view(request):
    faculty_list = Faculty.objects.all()
    context = dict(page_title='Accounts-Faculty', h1_title='Faculty', url='Faculty',
                   card_title="All Faculty", faculty_list=faculty_list)
    return render(request, 'accounts/faculty_list.html', context)


# student

def createStudent(request):
    if request.method == "GET":
        user_form = UserForm()
        faculty_form = StudentForm()
        context = dict(page_title='Accounts-Create Student', h1_title='New Student Account', url='createstudent',
                       card_title="Account Information", user_form=user_form, form=faculty_form)
        return render(request, 'accounts/student_create_form.html', context)
    else:
        registered = False
        user_form = UserForm(data=request.POST)
        student_form = StudentForm(data=request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user: User = user_form.save()
            user.set_password(user.password)
            user.save()
            student: Student = student_form.save(commit=False)
            student.user = user
            if 'profile_pic' in request.FILES:
                student.profile_pic = request.FILES['profile_pic']
            student.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            registered = True
        if registered:
            messages.success(request, 'Account created  Successfully')
            return redirect('accounts:students_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Create student', h1_title='New student Account', url='createstudent',
                           card_title="Account Information", user_form=user_form, form=student_form)
            return render(request, 'accounts/student_create_form.html', context)


def createStudentWithExistingUser(request, id=0):
    if id == 0:
        messages.error(request, 'Not user found against this id')
        return redirect('accounts:students_list')
    else:
        try:
            user: User = User.objects.get(pk=id)
        except user.DoesNotExist:
            messages.error(request, 'User Not found against id or In-Valid id')
            return redirect('accounts:students_list')

        if Student.objects.filter(user=user).exists():
            messages.error(request, 'Student With This Account Already Exist')
            group = Group.objects.get(name='student')
            user.groups.add(group)
            messages.info(request, 'User is Added in Student Group')
            return redirect('accounts:students_list')

    if request.method == "GET":
        student_form = StudentForm()
        context = dict(page_title='Accounts-Create Student', h1_title='New Student Account', url='createstudent',
                       card_title="Account Information", form=student_form, id=id)
        return render(request, 'accounts/student_create_form_with_existing_user.html', context)
    else:
        registered = False
        student_form = StudentForm(data=request.POST)
        if student_form.is_valid():
            student: Student = student_form.save(commit=False)
            student.user = user
            if 'profile_pic' in request.FILES:
                student.profile_pic = request.FILES['profile_pic']
            student.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            registered = True
        if registered:
            messages.success(request, 'Account created  Successfully')
            return redirect('accounts:students_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Create student', h1_title='New student Account', url='createstudent',
                           card_title="Account Information", form=student_form, id=id)
            return render(request, 'accounts/student_create_form_with_existing_user.html', context)


def edit_student(request, id=0):
    if id == 0:
        messages.error(request, 'Not student found against this id')
        return redirect('accounts:students_list')
    else:
        try:
            student: Student = Student.objects.get(pk=id)
        except student.DoesNotExist:
            messages.error(request, 'Student Not found against id or In-Valid id')
            return redirect('accounts:students_list')
    if request.method == "GET":
        form = StudentForm(instance=student)
        context = dict(page_title='Accounts-Edit Student', h1_title='Edit Student', url='editstudent',
                       card_title="Account Information", form=form, id=id)
        return render(request, 'accounts/student_form.html', context)
    else:
        pic = student.profile_pic
        registered = False
        form = StudentForm(data=request.POST, instance=student,files=request.FILES)
        if form.is_valid():

            student = form.save()
            registered = True
        if registered:
            messages.success(request, 'Account created  Successfully')
            return redirect('accounts:students_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Edit Student', h1_title='Edit Student', url='editstudent',
                           card_title="Account Information", form=form, id=id)
            return render(request, 'accounts/student_form.html', context)


def student_list_view(request):
    student_list = Student.objects.all()
    context = dict(page_title='Accounts-Students', h1_title='Students', url='Students',
                   card_title="All Students", student_list=student_list)
    return render(request, 'accounts/student_list.html', context)


# User

def user_list_view(request):
    user_list = User.objects.all()
    context = dict(page_title='Accounts-Users', h1_title='All Users', url='users',
                   card_title="All Users", user_list=user_list)
    return render(request, 'accounts/user_list.html', context)


def un_active_user(request, id=0):
    if id > 0:
        try:
            user: User = User.objects.get(pk=id)
            if user.is_active:
                user.is_active = False
                user.save()
                messages.success(request, 'User is un-active now')
            else:
                messages.info(request, 'user is already Un Active')

        except user.DoesNotExist:
            messages.error(request, 'User Not found against id or In-Valid id')
    else:
        messages.error(request, 'User Not found against id or In-Valid id')
    return redirect('accounts:users_list')


def active_user(request, id=0):
    if id > 0:
        try:
            user: User = User.objects.get(pk=id)
            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, 'User is active now')
            else:
                messages.info(request, 'user is already Active')

        except user.DoesNotExist:
            messages.error(request, 'User Not found against id or In-Valid id')
    else:
        messages.error(request, 'User Not found against id or In-Valid id')

    return redirect('accounts:users_list')


def edit_user(request, id=0):
    if id == 0:
        messages.error(request, 'Not user found against this id')
        return redirect('accounts:users_list')
    else:
        try:
            user: User = User.objects.get(pk=id)
        except user.DoesNotExist:
            messages.error(request, 'User Not found against id or In-Valid id')
            return redirect('accounts:users_list')
    if request.method == "GET":
        form = UserForm(instance=user)
        context = dict(page_title='Accounts-Edit User', h1_title='Edit User', url='edituser',
                       card_title="Account Information", form=form, id=id)
        return render(request, 'accounts/user_form.html', context)
    else:
        registered = False
        form = UserForm(data=request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        if registered:
            messages.success(request, 'Account created  Successfully')
            return redirect('accounts:users_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Edit User', h1_title='Edit User', url='edituser',
                           card_title="Account Information", form=form, id=id)
            return render(request, 'accounts/user_form.html', context)


# change password
@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('accounts:change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    context = dict(page_title='Accounts-Change Password', h1_title='Change Password', url='change_password',
                   card_title="All Students", form=form)
    return render(request, 'accounts/change_password.html', context)
