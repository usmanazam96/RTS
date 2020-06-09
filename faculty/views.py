from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.shortcuts import render, redirect

from RTS.decorators import allowed_users
from accounts.forms import FacultyForm
from faculty.forms import FacultyAvailabilityForm, ScheduleForm
from faculty.models import FacultyAvailability, Schedule

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from faculty.queries import *


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
    availability = FacultyAvailability.objects.get(faculty=request.user.faculty)
    form = FacultyAvailabilityForm(instance=availability)
    context = dict(page_title='Faculty-Availability', h1_title='Faculty Availability', url='Faculty Availability',
                   availability=availability, form=form)
    return render(request, 'faculty/faculty_availability.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def update_status(request):
    availability = FacultyAvailability.objects.get(faculty=request.user.faculty)
    print("enter")
    print(availability.availabilityMsg)
    print(availability.availability)
    updated = False
    form = FacultyAvailabilityForm(data=request.POST, instance=availability)
    if form.is_valid():
        form.save()
        updated = True
    if updated:
        messages.success(request, 'Account updated  Successfully')
        return redirect('faculty:availability_status')
    else:
        messages.error(request, 'Invalid Information.Check the  Wrong Information')
        context = dict(page_title='Faculty-Availability', h1_title='Faculty Availability', url='Faculty Availability',
                       availability=availability, form=form)
        return render(request, 'faculty/faculty_availability.html', context)


def available_status_on_faculty(request):
    faculty_availability = FacultyAvailability.objects.filter(availability=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(faculty_availability, 10)
    try:
        faculty_availability = paginator.page(page)
    except PageNotAnInteger:
        faculty_availability = paginator.page(1)
    except EmptyPage:
        faculty_availability = paginator.page(paginator.num_pages)
    context = dict(page_title='Faculty-Availability', h1_title='Available', url='Available Faculty',
                   faculty_availability=faculty_availability)
    return render(request, 'faculty/all_faculty_availability.html', context)


def available_status_off_faculty(request):
    faculty_availability = FacultyAvailability.objects.filter(availability=False)
    page = request.GET.get('page', 1)
    paginator = Paginator(faculty_availability, 10)
    try:
        faculty_availability = paginator.page(page)
    except PageNotAnInteger:
        faculty_availability = paginator.page(1)
    except EmptyPage:
        faculty_availability = paginator.page(paginator.num_pages)
    context = dict(page_title='Faculty-Availability', h1_title='Not Available', url='Not Available Faculty',
                   faculty_availability=faculty_availability)
    return render(request, 'faculty/all_faculty_availability.html', context)


def all_available_faculty(request):
    faculty_availability = FacultyAvailability.objects.all().order_by('-availability')
    page = request.GET.get('page', 1)

    paginator = Paginator(faculty_availability, 10)
    try:
        faculty_availability = paginator.page(page)
    except PageNotAnInteger:
        faculty_availability = paginator.page(1)
    except EmptyPage:
        faculty_availability = paginator.page(paginator.num_pages)
    context = dict(page_title='All-Faculty', h1_title='All Faculty', url='All Faculty',
                   faculty_availability=faculty_availability)
    return render(request, 'faculty/all_faculty_availability.html', context)


def search_availability_faculty(request):
    query = request.GET.get('query')
    first_name_q = Q(faculty__first_name__icontains=query)
    last_name_q = Q(faculty__last_name__icontains=query)
    faculty_availability = FacultyAvailability.objects.filter(first_name_q | last_name_q
                                                              ).order_by(
        '-availability')
    page = request.GET.get('page', 1)

    paginator = Paginator(faculty_availability, 10)
    try:
        faculty_availability = paginator.page(page)
    except PageNotAnInteger:
        faculty_availability = paginator.page(1)
    except EmptyPage:
        faculty_availability = paginator.page(paginator.num_pages)
    context = dict(page_title='All-Faculty', query=query, h1_title=f'Result for  {query}', url='All Faculty',
                   faculty_availability=faculty_availability)
    return render(request, 'faculty/all_faculty_availability.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def schedule_view(request):
    schedule_list = Schedule.objects.filter(faculty=request.user.faculty).order_by('day', 'schedule_type', 'start_time')
    form = ScheduleForm()
    context = dict(page_title='Faculty-Availability', h1_title='Faculty Availability', url='Faculty Availability',
                   schedule_list=schedule_list, form=form)
    return render(request, 'faculty/schedule.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def schedule_create(request):
    if request.method == 'GET':
        schedule_form = ScheduleForm(request.GET)
    else:
        schedule_form = ScheduleForm(request.POST)
    form_valid = schedule_form.is_valid()
    start_time_valid = False
    end_time_valid = False
    faculty = request.user.faculty
    if form_valid:
        start_time = schedule_form.cleaned_data['start_time']
        end_time = schedule_form.cleaned_data['end_time']
        day = schedule_form.cleaned_data['day']

        end_time_valid = is_valid_schedule_time(end_time, day, faculty)
        print(f'day {day} start_time{start_time} end_time{end_time}')
        start_time_valid = is_valid_schedule_time(start_time, day, faculty)
        if not start_time_valid:
            schedule_form.add_start_time_clash_error()
        if not end_time_valid:
            schedule_form.add_end_time_clash_error()

    if form_valid and start_time_valid and end_time_valid:
        """schedule = schedule_form.save(commit=False)
        schedule.faculty = request.user.faculty
        schedule.save()"""
        messages.success(request, 'Schedule Added Successfully')
        return redirect('faculty:schedule_view')
    else:
        schedule_list = Schedule.objects.filter(faculty=request.user.faculty).order_by('day').order_by('-start_time')
        form = schedule_form
        messages.error(request, 'There are errors. please check')
        context = dict(page_title='Faculty-Availability', h1_title='Faculty Availability', url='Faculty Availability',
                       schedule_list=schedule_list, form=form)
        return render(request, 'faculty/schedule.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def schedule_update(request, id=0):
    if id < 1:
        messages.info(request, 'In Valid Id')
        return redirect('faculty:schedule_view')
    try:
        schedule = Schedule.objects.get(id=id)
    except Schedule.DoesNotExist:
        messages.info(request, 'Schedule Does not Exist')
        return redirect('faculty:schedule_view')
    if schedule.faculty != request.user.faculty:
        messages.info(request, 'In valid id that schedule does not belongs to you')
        return redirect('faculty:schedule_view')
    if request.method == 'GET':
        schedule_form = ScheduleForm(instance=schedule)
        context = dict(page_title='Faculty-Availability', h1_title='Faculty Availability', url='Faculty Availability',
                       form=schedule_form, id=id)
        return render(request, 'faculty/schedule_update.html', context)
    else:
        schedule_form = ScheduleForm(request.POST, instance=schedule)
        form_valid = schedule_form.is_valid()
        start_time_valid = False
        end_time_valid = False
        faculty = request.user.faculty
        if form_valid:
            start_time = schedule_form.cleaned_data['start_time']
            end_time = schedule_form.cleaned_data['end_time']
            day = schedule_form.cleaned_data['day']

            end_time_valid = is_valid_schedule_time(end_time, day, faculty, id)
            start_time_valid = is_valid_schedule_time(start_time, day, faculty, id)
            if not start_time_valid:
                schedule_form.add_start_time_clash_error()
            if not end_time_valid:
                schedule_form.add_end_time_clash_error()

        if form_valid and start_time_valid and end_time_valid:
            schedule = schedule_form.save()
            """schedule.faculty = request.user.faculty
            schedule.save()"""
            messages.success(request, 'Schedule Updated Successfully')
            return redirect('faculty:schedule_view')
        else:
            schedule_list = Schedule.objects.filter(faculty=request.user.faculty).order_by('day').order_by(
                '-start_time')
            form = schedule_form
            messages.error(request, 'There are errors. please check')
            context = dict(page_title='Faculty-Availability', h1_title='Faculty Availability',
                           url='Faculty Availability',
                           form=schedule_form, id=id)
            return render(request, 'faculty/schedule_update.html', context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def schedule_remove(request, id=0):
    if id < 1:
        messages.info(request, 'In Valid Id')
        return redirect('faculty:schedule_view')
    try:
        schedule = Schedule.objects.get(id=id)
    except Schedule.DoesNotExist:
        messages.info(request, 'Schedule Does not Exist')
        return redirect('faculty:schedule_view')
    if schedule.faculty != request.user.faculty:
        messages.info(request, 'In valid id that schedule does not belongs to you')
        return redirect('faculty:schedule_view')
    schedule.delete()
    messages.success(request, f'Schedule removed Successfully')
    return redirect('faculty:schedule_view')
