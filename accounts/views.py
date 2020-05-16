from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.http import HttpResponse

from django.shortcuts import render, redirect

# Create your views here.
from accounts.decorators import unauthenticated_user

from accounts.models import *
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


def student_list_view(request):
    student_list = Student.objects.all()
    context = dict(page_title='Accounts-Students', h1_title='Students', url='Students',
                   card_title="All Students", student_list=student_list)
    return render(request, 'accounts/student_list.html', context)
