from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.shortcuts import render, redirect

from RTS.decorators import allowed_users
from accounts.forms import FacultyForm
from faculty.forms import FacultyAvailabilityForm
from faculty.models import FacultyAvailability


# Create your views here.
def home(request):
    faculty_availability = FacultyAvailability.objects.all()
    context = dict(faculty_availability=faculty_availability)
    return render(request, 'faculty/index.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def profile(request):
    faculty = request.user.faculty
    context = dict(page_title='Faculty-Profile', h1_title='Faculty Profile', url='Faculty profile', faculty=faculty)
    return render(request, 'faculty/profile.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def edit_profile(request):
    faculty = request.user.faculty
    if request.method == "GET":
        form = FacultyForm(instance=faculty)
        context = dict(page_title='Administration-Profile Edit', h1_title='Edit Profile', url='edit_faculty',
                       card_title="Account Information", form=form)
        return render(request, 'faculty/profile_form.html', context)
    else:
        updated = False
        form = FacultyForm(data=request.POST, instance=faculty, files=request.FILES)
        if form.is_valid():
            admin = form.save()
            updated = True
        if updated:
            messages.success(request, 'Account updated  Successfully')
            return redirect('faculty:profile')
        else:
            messages.error(request, 'Invalid Information.Check the  Wrong Information')
            context = dict(page_title='Administration-Profile Edit', h1_title='Edit Profile', url='editprofile',
                           card_title="Account Information", form=form)
            return render(request, 'administration/profile_form.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def availability_status(request):
    availability = FacultyAvailability(faculty=request.user.faculty)
    form = FacultyAvailabilityForm(instance=availability)
    context = dict(page_title='Faculty-Availability', h1_title='Faculty Availability', url='Faculty Availability',
                   availability=availability, form=form)
    return render(request, 'faculty/faculty_availability.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def update_status(request):
    availability = FacultyAvailability(faculty=request.user.faculty)
    updated = False
    form = FacultyAvailabilityForm(data=request.POST, instance=availability)
    if form.is_valid():
        admin = form.save()
        updated = True
    if updated:
        messages.success(request, 'Account updated  Successfully')
        context = dict(page_title='Faculty-Availability', h1_title='Faculty Availability', url='Faculty Availability',
                       availability=availability, form=form)
        return render(request, 'faculty/faculty_availability.html', context)
    else:
        messages.error(request, 'Invalid Information.Check the  Wrong Information')
        context = dict(page_title='Faculty-Availability', h1_title='Faculty Availability', url='Faculty Availability',
                       availability=availability, form=form)
        return render(request, 'faculty/faculty_availability.html', context)
