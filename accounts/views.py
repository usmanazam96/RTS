from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
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


def createAdmin(request):
    if request.method == "GET":
        user_form = UserForm()
        faculty_form = AdminForm()
        context = dict(page_title='Admin-Create Faculty', h1_title='New Admin Account', url='createfaculty',
                       card_title="Account Information", user_form=user_form, form=faculty_form)
        return render(request, 'accounts/admin_create_form.html', context)
    else:
        return HttpResponse('post')


def createStudent(request):
    if request.method == "GET":
        user_form = UserForm()
        faculty_form = StudentForm()
        context = dict(page_title='Accounts-Create Student', h1_title='New Faculty Account', url='createstudent',
                       card_title="Account Information", user_form=user_form, form=faculty_form)
        return render(request, 'accounts/student_create_form.html', context)
    else:
        return HttpResponse('post')


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
                faculty.profile_pic = request.FILES('profile_pic')
            faculty.save()
            faculty_availability = FacultyAvailability(faculty=faculty)
            faculty_availability.save()
            registered = True
        if registered:
            messages.success(request, 'Subject Status Changed Successfully')
            # return redirect('administration:all Faculty')
            return HttpResponse('done')
        else:
            messages.error(request, 'Information wrong')
            context = dict(page_title='Accounts-Create Faculty', h1_title='New Faculty Account', url='createfaculty',
                           card_title="Account Information", user_form=user_form, form=faculty_form)
            return render(request, 'accounts/faculty_create_form.html', context)
