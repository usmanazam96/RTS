from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from RTS.decorators import allowed_users
from student.forms import StudentForm
from accounts.forms import Student
from student.queries import dashboard


# Create your views here.

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['student'])
def home(request):
    context = dict(page_title='Student-Dashboard', h1_title='Student Dashboard', url='dashboard',
                   student_home='active')
    context.update(dashboard(request.user.student))

    return render(request, 'student/index.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['student'])
def profile(request):
    student = request.user.student
    context = dict(page_title='Student-Profile', h1_title='Student Profile', url='student profile', student=student,
                   student_my_profile_li='active', my_account_ul='menu-open')
    return render(request, 'student/profile.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['student'])
def edit_profile(request):
    student = request.user.student
    if request.method == "GET":
        form = StudentForm(instance=student)
        context = dict(page_title='Administration-Profile Edit', h1_title='Edit Profile', url='editadmin',
                       card_title="Account Information", form=form,
                       student_my_edit_profile_li='active', my_account_ul='menu-open')
        return render(request, 'student/profile_form.html', context)
    else:
        updated = False
        form = StudentForm(data=request.POST, instance=student, files=request.FILES)
        if form.is_valid():
            admin = form.save()
            updated = True
        if updated:
            messages.success(request, 'Account updated  Successfully')
            return redirect('student:profile')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Student-Profile Edit', h1_title='Edit Profile', url='editprofile',
                           card_title="Account Information", form=form,
                           student_my_edit_profile_li='active', my_account_ul='menu-open')
            return render(request, 'student/profile_form.html', context)


@login_required(login_url='accounts:login')
def student_profile_visitor(request, id=0):
    if id <= 0:
        messages.error(request, 'Student Not found against this id')
        return redirect('accounts:home')
    else:
        try:
            student: Student = Student.objects.get(pk=id)
        except Student.DoesNotExist:
            messages.error(request, 'Student Not found against this id')
            return redirect('index')
        context = dict(page_title='Student-Student Profile', h1_title='Faculty Profile', url='Student Profile',
                       card_title="Account Information",
                       student=student)
    return render(request, 'student/student_profile_visitor.html', context)
