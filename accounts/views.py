from typing import Dict

from django.contrib import messages
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render, redirect

# Create your views here.
from RTS.decorators import unauthenticated_user, allowed_users

from faculty.models import *

from accounts.forms import *


def home(request):
    role = request.session.get('login_role', 'None')
    if role == "admin":
        return redirect('administration:home')
    if role == "faculty":
        return redirect('faculty:faculty home')
    if role == "student":
        return redirect('student:student home')
    logout(request)
    return redirect('index')


"""
    l = request.user.groups.values_list('name', flat=True)  # QuerySet Object
    list1 = list(l)
    count = request.user.groups.count()
    list2 = ['student', 'faculty', 'admin']
    list3 = list(set(list1).intersection(list2))
    context = dict(groups=list1, allow=list2, common=list3, count=count, role=role)
    return render(request, 'accounts/home.html', context)
    """


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                count = user.groups.count()
                if count < 1:
                    messages.info(request, f"{username} has not any group. kindly connect with admin")
                else:
                    login(request, user)
                    if count > 1:
                        return redirect('accounts:login_role_select')
                    else:
                        group = request.user.groups.all()[0].name
                        request.session['login_role'] = group
                        messages.success(request, f'login as {group} ')
                        return redirect('accounts:home')
            else:
                messages.error(request, f'Account belong to  {username} '
                                        f'is un active.kindly connect with admin')
        else:
            try:
                user = User.objects.get(username=username)
                if user.is_active:
                    messages.error(request, 'Wrong Password')
                else:
                    messages.error(request, f'Account belong to   {username} '
                                            f'is un active.kindly connect with admin')

            except User.DoesNotExist:
                messages.error(request, f'Not Account belong to {username}')

    context = {'title': 'accounts | login'}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='accounts:login')
def login_role_select(request):
    if request.method == 'GET':
        if request.user.groups.count() == 1:
            return redirect('accounts:home')
        groups = request.user.groups.all()
        context = dict(title='accounts | login-role', groups=groups)
        return render(request, 'accounts/login_role_select.html', context)

    else:
        group_id = request.POST.get('role')
        try:
            group = request.user.groups.get(pk=group_id)
            request.session['login_role'] = group.name
            messages.success(request, f'login as {group.name} ')
            return redirect('accounts:home')
        except Group.DoesNotExist:
            messages.info(request, 'You are selecting wrong group')
            groups = request.user.groups.all()
            context = dict(title='accounts | login-role', groups=groups)
            return render(request, 'accounts/login_role_select.html', context)


def logoutUser(request):
    logout(request)
    return redirect('accounts:login')


# admin
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def createAdmin(request):
    if request.method == "GET":
        user_form = UserForm()
        admin_form = AdminForm()
        context = dict(page_title='Admin-Create Faculty', h1_title='New Admin Account', url='createfaculty',
                       card_title="Account Information", user_form=user_form, form=admin_form,
                       create_admin_li='active', admin_ul='menu-open')
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


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def edit_admin(request, id=0):
    if id == 0:
        messages.error(request, 'Not admin found against this id')
        return redirect('accounts:admins_list')
    else:
        try:
            admin: Admin = Admin.objects.get(pk=id)
        except admin.DoesNotExist:
            messages.error(request, 'Admin Not found against id or In-Valid id')
            return redirect('accounts:admins_list')
    if request.method == "GET":
        form = AdminForm(instance=admin)
        context = dict(page_title='Accounts-Edit Admin', h1_title='Edit Admin', url='editadmin',
                       card_title="Account Information", form=form, id=id)
        return render(request, 'accounts/admin_form.html', context)
    else:
        pic = admin.profile_pic
        registered = False
        form = AdminForm(data=request.POST, instance=admin, files=request.FILES)
        if form.is_valid():
            admin = form.save()
            registered = True
        if registered:
            messages.success(request, 'Account created  Successfully')
            return redirect('accounts:admins_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Edit Admin', h1_title='Edit Admin', url='editadmin',
                           card_title="Account Information", form=form, id=id)
            return render(request, 'accounts/admin_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def admin_list_view(request):
    admin_list = Admin.objects.all()
    context = dict(page_title='Accounts-Admins', h1_title='Admins', url='Admins',
                   card_title="All Admins", admin_list=admin_list, next_page='admins',
                   admin_list_li='active', admin_ul='menu-open')
    return render(request, 'accounts/admin_list.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def createAdminWithExistingUser(request, id=0):
    page = request.GET.get('next_page', 'admins')
    if id == 0:
        messages.error(request, 'Not user found against this id')
        return redirect('accounts:admins_list')
    else:
        try:
            user: User = User.objects.get(pk=id)
        except user.DoesNotExist:
            messages.error(request, 'User Not found against id or In-Valid id')
            if page == 'users':
                return redirect('accounts:users_list')
            elif page == 'active_users':
                return redirect('accounts:active_users_list')
            elif page == 'in_active_users':
                return redirect('accounts:un_active_users_list')
            elif page == 'students':
                return redirect('accounts:students_list')
            elif page == 'admins':
                return redirect('accounts:admins_list')
            elif page == 'faculty':
                return redirect('accounts:faculty_list')
            return redirect('accounts:admins_list')

        if Admin.objects.filter(user=user).exists():
            messages.info(request, 'Admin With This Account Already Exist')
            messages.info(request, 'user added in Admin group again')
            group = Group.objects.get(name='admin')
            user.groups.add(group)
            messages.info(request, 'User is Added in Admin Group')
            return redirect('accounts:admins_list')

    if request.method == "GET":
        admin_form = AdminForm()
        context = dict(page_title='Accounts-Create Admin', h1_title='New Admin Account', url='createadmin',
                       card_title="Account Information", form=admin_form, id=id, next_page=page)
        return render(request, 'accounts/admin_create_form_with_existing_user.html', context)
    else:
        registered = False
        admin_form = AdminForm(data=request.POST)
        if admin_form.is_valid():
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
            return redirect('accounts:admins_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Create admin', h1_title='New admin Account', url='createadmin',
                           card_title="Account Information", form=admin_form, id=id, next_page=page)
            return render(request, 'accounts/admin_create_form_with_existing_user.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def remove_admin_group(request, id):
    page = request.GET.get('next_page', 'users')
    if id > 0:
        try:
            user: User = User.objects.get(pk=id)
            if user.groups.filter(name='admin').exists():
                group = Group.objects.get(name='admin')
                user.groups.remove(group)
                messages.info(request, 'admin group is removed')
            else:
                messages.info(request, 'admin group is already removed')

        except User.DoesNotExist:
            messages.error(request, 'User Not found against id or In-Valid id')
    else:
        messages.error(request, 'User Not found against id or In-Valid id')
    if page == 'users':
        return redirect('accounts:users_list')
    elif page == 'active_users':
        return redirect('accounts:active_users_list')
    elif page == 'in_active_users':
        return redirect('accounts:un_active_users_list')
    elif page == 'students':
        return redirect('accounts:students_list')
    elif page == 'admins':
        return redirect('accounts:admins_list')
    elif page == 'faculty':
        return redirect('accounts:faculty_list')
    return redirect('accounts:users_list')


# faculty

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def createFaculty(request):
    if request.method == "GET":
        user_form = UserForm()
        faculty_form = FacultyForm()
        context = dict(page_title='Accounts-Create Faculty', h1_title='New Faculty Account', url='createfaculty',
                       card_title="Account Information", user_form=user_form, form=faculty_form,
                       create_faculty_li='active', faculty_ul='menu-open')
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
                           card_title="Account Information", user_form=user_form, form=faculty_form,
                           create_faculty_li='active', faculty_ul='menu-open')
            return render(request, 'accounts/faculty_create_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def faculty_list_view(request):
    faculty_list = Faculty.objects.all()
    context = dict(page_title='Accounts-Faculty', h1_title='Faculty', url='Faculty',
                   card_title="All Faculty", faculty_list=faculty_list, next_page='faculty',
                   faculty_list_li='active', faculty_ul='menu-open')
    return render(request, 'accounts/faculty_list.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def edit_faculty(request, id=0):
    if id == 0:
        messages.error(request, 'Not faculty found against this id')
        return redirect('accounts:faculty_list')
    else:
        try:
            faculty: Faculty = Faculty.objects.get(pk=id)
        except faculty.DoesNotExist:
            messages.error(request, 'Faculty Not found against id or In-Valid id')
            return redirect('accounts:faculty_list')
    if request.method == "GET":
        form = FacultyForm(instance=faculty)
        context = dict(page_title='Accounts-Edit Faculty', h1_title='Edit Faculty', url='editfaculty',
                       card_title="Account Information", form=form, id=id)
        return render(request, 'accounts/faculty_form.html', context)
    else:
        pic = faculty.profile_pic
        registered = False
        form = FacultyForm(data=request.POST, instance=faculty, files=request.FILES)
        if form.is_valid():
            faculty = form.save()
            registered = True
        if registered:
            messages.success(request, 'Account created  Successfully')
            return redirect('accounts:faculty_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Edit Faculty', h1_title='Edit Faculty', url='editfaculty',
                           card_title="Account Information", form=form, id=id)
            return render(request, 'accounts/faculty_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def createFacultyWithExistingUser(request, id=0):
    page = request.GET.get('next_page', 'faculty')
    if id == 0:
        messages.error(request, 'Not user found against this id')
        return redirect('accounts:faculty_list')
    else:
        try:
            user: User = User.objects.get(pk=id)
        except user.DoesNotExist:
            messages.error(request, 'User Not found against id or In-Valid id')
            return redirect('accounts:faculty_list')

        if Faculty.objects.filter(user=user).exists():
            messages.info(request, 'Faculty With This Account Already Exist')
            messages.info(request, 'user added in Faculty group again')
            group = Group.objects.get(name='faculty')
            user.groups.add(group)
            messages.info(request, 'User is Added in Faculty Group')
            if page == 'users':
                return redirect('accounts:users_list')
            elif page == 'active_users':
                return redirect('accounts:active_users_list')
            elif page == 'in_active_users':
                return redirect('accounts:un_active_users_list')
            elif page == 'students':
                return redirect('accounts:students_list')
            elif page == 'admins':
                return redirect('accounts:admins_list')
            elif page == 'faculty':
                return redirect('accounts:faculty_list')
            return redirect('accounts:faculty_list')

    if request.method == "GET":
        faculty_form = FacultyForm()
        context = dict(page_title='Accounts-Create Faculty', h1_title='New Faculty Account', url='createfaculty',
                       card_title="Account Information", form=faculty_form, id=id, next_page=page,
                       )
        return render(request, 'accounts/faculty_create_form_with_existing_user.html', context)
    else:
        registered = False
        faculty_form = FacultyForm(data=request.POST)
        if faculty_form.is_valid():
            faculty: Faculty = faculty_form.save(commit=False)
            faculty.user = user
            if 'profile_pic' in request.FILES:
                faculty.profile_pic = request.FILES['profile_pic']
            faculty.save()
            group = Group.objects.get(name='faculty')
            user.groups.add(group)
            registered = True
        if registered:
            messages.success(request, 'Account created  Successfully')
            if page == 'users':
                return redirect('accounts:users_list')
            elif page == 'active_users':
                return redirect('accounts:active_users_list')
            elif page == 'in_active_users':
                return redirect('accounts:un_active_users_list')
            elif page == 'students':
                return redirect('accounts:students_list')
            elif page == 'admins':
                return redirect('accounts:admins_list')
            elif page == 'faculty':
                return redirect('accounts:faculty_list')
            return redirect('accounts:faculty_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Create faculty', h1_title='New faculty Account', url='createfaculty',
                           card_title="Account Information", form=faculty_form, id=id, next_page=page)
            return render(request, 'accounts/faculty_create_form_with_existing_user.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def remove_faculty_group(request, id):
    page = request.GET.get('next_page', 'users')
    if id > 0:
        try:
            user: User = User.objects.get(pk=id)
            if user.groups.filter(name='faculty').exists():
                group = Group.objects.get(name='faculty')
                user.groups.remove(group)
                messages.info(request, 'faculty group is removed')
            else:
                messages.info(request, 'faculty group is already removed')

        except User.DoesNotExist:
            messages.error(request, 'User Not found against id or In-Valid id')
    else:
        messages.error(request, 'User Not found against id or In-Valid id')
    if page == 'users':
        return redirect('accounts:users_list')
    elif page == 'active_users':
        return redirect('accounts:active_users_list')
    elif page == 'in_active_users':
        return redirect('accounts:un_active_users_list')
    elif page == 'students':
        return redirect('accounts:students_list')
    elif page == 'admins':
        return redirect('accounts:admins_list')
    elif page == 'faculty':
        return redirect('accounts:faculty_list')
    return redirect('accounts:users_list')


@login_required(login_url='accounts:login')
def faculty_profile(request, id=0):
    if id <= 0:
        messages.error(request, 'Not faculty found against this id')
        return redirect('accounts:faculty_list')
    else:
        try:
            faculty: Faculty = Faculty.objects.get(pk=id)
        except Faculty.DoesNotExist:
            messages.error(request, 'Faculty Not found against id or In-Valid id')
            return redirect('accounts:faculty_list')
        context = dict(page_title='Accounts-Faculty Profile', h1_title='Faculty Profile', url='faculty_profile',
                       card_title="Account Information", faculty_profile_li='active', faculty_profile_ul='menu-open',
                       faculty=faculty)
    return render(request, 'accounts/faculty_profile.html', context)


def faculty_profile_visitor(request, id=0):
    if id <= 0:
        messages.error(request, 'Not faculty found against this id')
        return redirect('index')
    else:
        try:
            faculty: Faculty = Faculty.objects.get(pk=id)
        except Faculty.DoesNotExist:
            messages.error(request, 'Faculty Not found against id or In-Valid id')
            return redirect('index')
        context = dict(page_title='Accounts-Faculty Profile', h1_title='Faculty Profile', url='faculty_profile',
                       card_title="Account Information", faculty_profile_visitori='active',
                       faculty_profile_visitor='menu-open',
                       faculty=faculty)
    return render(request, 'accounts/faculty_profile_visitor.html', context)


# student
@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def createStudent(request):
    if request.method == "GET":
        user_form = UserForm()
        faculty_form = StudentForm()
        context = dict(page_title='Accounts-Create Student', h1_title='New Student Account', url='createstudent',
                       card_title="Account Information", user_form=user_form, form=faculty_form,
                       create_student_li='active', student_ul='menu-open')
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
                           card_title="Account Information", user_form=user_form, form=student_form,
                           create_student_li='active', student_ul='menu-open'
                           )
            return render(request, 'accounts/student_create_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def createStudentWithExistingUser(request, id=0):
    page = request.GET.get('next_page', 'students')
    if id == 0:
        messages.error(request, 'Not user found against this id')
        return redirect('accounts:students_list')
    else:
        try:
            user: User = User.objects.get(pk=id)
        except user.DoesNotExist:
            messages.error(request, 'User Not found against id or In-Valid id')
            if page == 'users':
                return redirect('accounts:users_list')
            elif page == 'active_users':
                return redirect('accounts:active_users_list')
            elif page == 'in_active_users':
                return redirect('accounts:un_active_users_list')
            elif page == 'students':
                return redirect('accounts:students_list')
            elif page == 'admins':
                return redirect('accounts:admins_list')
            elif page == 'faculty':
                return redirect('accounts:faculty_list')
            return redirect('accounts:students_list')

        if Student.objects.filter(user=user).exists():
            messages.info(request, 'Student With This Account Already Exist')
            messages.info(request, 'user added in student group again')
            group = Group.objects.get(name='student')
            user.groups.add(group)
            messages.info(request, 'User is Added in Student Group')
            if page == 'users':
                return redirect('accounts:users_list')
            elif page == 'active_users':
                return redirect('accounts:active_users_list')
            elif page == 'in_active_users':
                return redirect('accounts:un_active_users_list')
            elif page == 'students':
                return redirect('accounts:students_list')
            elif page == 'admins':
                return redirect('accounts:admins_list')
            elif page == 'faculty':
                return redirect('accounts:faculty_list')
            return redirect('accounts:students_list')

    if request.method == "GET":
        student_form = StudentForm()
        context = dict(page_title='Accounts-Create Student', h1_title='New Student Account', url='createstudent',
                       card_title="Account Information", form=student_form, id=id, next_page=page,
                       student_ul='menu-open')
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
            if page == 'users':
                return redirect('accounts:users_list')
            elif page == 'active_users':
                return redirect('accounts:active_users_list')
            elif page == 'in_active_users':
                return redirect('accounts:un_active_users_list')
            elif page == 'students':
                return redirect('accounts:students_list')
            elif page == 'admins':
                return redirect('accounts:admins_list')
            elif page == 'faculty':
                return redirect('accounts:faculty_list')
            return redirect('accounts:students_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Create student', h1_title='New student Account', url='createstudent',
                           card_title="Account Information", form=student_form, id=id, next_page=page,
                           student_ul='menu-open')
            return render(request, 'accounts/student_create_form_with_existing_user.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
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
                       card_title="Account Information", form=form, id=id,
                       student_ul='menu-open')
        return render(request, 'accounts/student_form.html', context)
    else:
        pic = student.profile_pic
        registered = False
        form = StudentForm(data=request.POST, instance=student, files=request.FILES)
        if form.is_valid():
            student = form.save()
            registered = True
        if registered:
            messages.success(request, 'Account created  Successfully')
            return redirect('accounts:students_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Edit Student', h1_title='Edit Student', url='editstudent',
                           card_title="Account Information", form=form, id=id,
                           student_ul='menu-open')
            return render(request, 'accounts/student_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def student_list_view(request):
    student_list = Student.objects.all()
    context = dict(page_title='Accounts-Students', h1_title='Students', url='Students',
                   card_title="All Students", student_list=student_list, next_page='students',
                   student_list_li='active', student_ul='menu-open'
                   )
    return render(request, 'accounts/student_list.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def remove_student_group(request, id):
    page = request.GET.get("next_page", 'users')
    if id > 0:
        try:
            user: User = User.objects.get(pk=id)
            if user.groups.filter(name='student').exists():
                group = Group.objects.get(name='student')
                user.groups.remove(group)
                messages.info(request, 'student group is removed')
            else:
                messages.info(request, 'student group is already removed')

        except User.DoesNotExist:
            messages.error(request, 'User Not found against id or In-Valid id')
    else:
        messages.error(request, 'User Not found against id or In-Valid id')
    if page == 'users':
        return redirect('accounts:users_list')
    elif page == 'active_users':
        return redirect('accounts:active_users_list')
    elif page == 'in_active_users':
        return redirect('accounts:un_active_users_list')
    elif page == 'students':
        return redirect('accounts:students_list')
    elif page == 'admins':
        return redirect('accounts:admins_list')
    elif page == 'faculty':
        return redirect('accounts:faculty_list')
    return redirect('accounts:users_list')


@login_required(login_url='accounts:login')
def student_profile(request, id=0):
    if id <= 0:
        messages.error(request, 'Not faculty found against this id')
        return redirect('accounts:students_list')
    else:
        try:
            student: Student = Student.objects.get(pk=id)
        except Faculty.DoesNotExist:
            messages.error(request, 'Faculty Not found against id or In-Valid id')
            return redirect('accounts:faculty_list')
        context = dict(page_title='Accounts-Faculty Profile', h1_title='Student Profile', url='student_profile',
                       card_title="Account Information",
                       student=student, student_ul='menu-open')
    return render(request, 'accounts/student_profile.html', context)


# User


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def user_list_view(request):
    user_list = User.objects.all()
    context = dict(page_title='Accounts-Users', h1_title='All Users', url='users',
                   card_title="All Users", user_list=user_list, next_page='users',
                   users_list_li='active', users_ul='menu-open')
    return render(request, 'accounts/user_list.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def active_user_list_view(request):
    user_list = User.objects.filter(is_active=True)
    context = dict(page_title='Accounts-Users', h1_title='All Users', url='users',
                   card_title="All Users", user_list=user_list, next_page='active_users',
                   active_users_list_li='active', users_ul='menu-open')
    return render(request, 'accounts/user_list.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def un_active_user_list_view(request):
    user_list = User.objects.filter(is_active=False)
    context = dict(page_title='Accounts-Users', h1_title='All Users', url='users',
                   card_title="All Users", user_list=user_list, next_page='in_active_users',
                   un_active_users_list_li='active', users_ul='menu-open')
    return render(request, 'accounts/user_list.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def un_active_user(request, id=0, page='users'):
    page = request.GET.get('next_page', 'users')
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
    if page == 'users':
        return redirect('accounts:users_list')
    elif page == 'active_users':
        return redirect('accounts:active_users_list')
    elif page == 'in_active_users':
        return redirect('accounts:un_active_users_list')
    elif page == 'students':
        return redirect('accounts:students_list')
    elif page == 'admins':
        return redirect('accounts:admins_list')
    elif page == 'faculty':
        return redirect('accounts:faculty_list')
    return redirect('accounts:users_list')


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def active_user(request, id=0, page='users'):
    page = request.GET.get('next_page', 'users')
    if id > 0:
        try:
            user: User = User.objects.get(pk=id)
            if not user.is_active:
                user.is_active = True
                user.save()
                messages.success(request, 'User is active now')
            else:
                messages.info(request, 'user is already Active')

        except User.DoesNotExist:
            messages.error(request, 'User Not found against id or In-Valid id')
    else:
        messages.error(request, 'User Not found against id or In-Valid id')

    if page == 'users':
        return redirect('accounts:users_list')
    elif page == 'active_users':
        return redirect('accounts:active_users_list')
    elif page == 'in_active_users':
        return redirect('accounts:un_active_users_list')
    elif page == 'students':
        return redirect('accounts:students_list')
    elif page == 'admins':
        return redirect('accounts:admins_list')
    elif page == 'faculty':
        return redirect('accounts:faculty_list')
    return redirect('accounts:users_list')


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admin'])
def edit_user(request, id=0):
    page = request.GET.get('next_page', 'users')
    print(page)
    if id == 0:
        messages.error(request, 'Not user found against this id')
        if page == 'users':
            return redirect('accounts:users_list')
        elif page == 'active_users':
            return redirect('accounts:active_users_list')
        elif page == 'in_active_users':
            return redirect('accounts:un_active_users_list')
        elif page == 'students':
            return redirect('accounts:students_list')
        elif page == 'admins':
            return redirect('accounts:admins_list')
        elif page == 'faculty':
            return redirect('accounts:faculty_list')
        return redirect('accounts:users_list')
    else:
        try:
            user: User = User.objects.get(pk=id)
        except User.DoesNotExist:
            messages.error(request, 'User Not found against id or In-Valid id')
            if page == 'users':
                return redirect('accounts:users_list')
            elif page == 'active_users':
                return redirect('accounts:active_users_list')
            elif page == 'in_active_users':
                return redirect('accounts:un_active_users_list')
            elif page == 'students':
                return redirect('accounts:students_list')
            elif page == 'admins':
                return redirect('accounts:admins_list')
            elif page == 'faculty':
                return redirect('accounts:faculty_list')
            return redirect('accounts:users_list')
    if request.method == "GET":
        form = UserForm(instance=user)
        context = dict(page_title='Accounts-Edit User', h1_title='Edit User', url='edituser',
                       card_title="Account Information", form=form, id=id, next_page=page)
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
            if page == 'users':
                return redirect('accounts:users_list')
            elif page == 'active_users':
                return redirect('accounts:active_users_list')
            elif page == 'in_active_users':
                return redirect('accounts:un_active_users_list')
            elif page == 'students':
                return redirect('accounts:students_list')
            elif page == 'admins':
                return redirect('accounts:admins_list')
            elif page == 'faculty':
                return redirect('accounts:faculty_list')
            return redirect('accounts:users_list')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Accounts-Edit User', h1_title='Edit User', url='edituser',
                           card_title="Account Information", form=form, id=id, next_page=page)
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
                   card_title="All Students", form=form, my_account_ul='menu-open',
                   change_password_li='active')
    return render(request, 'accounts/change_password.html', context)
