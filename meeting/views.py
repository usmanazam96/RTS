from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from RTS.decorators import allowed_users
from meeting.models import *
from meeting.forms import *
from meeting.queries import *
from notifications.signals import notify


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['student', 'faculty'])
def send_meeting_request(request, id):
    if id <= 0:
        messages.error(request, 'Faculty not found against this id')
        return redirect('faculty:all_available_faculty_sidebar')
    else:
        try:
            faculty: Faculty = Faculty.objects.get(pk=id)
        except Faculty.DoesNotExist:
            messages.error(request, 'Faculty not found against this id')
            return redirect('faculty:all_available_faculty_sidebar')
    if request.method == 'GET':
        form = Meeting_Form()
        context = dict(page_title='Administration-Meeting Request', h1_title='Meeting Request',
                       url='Meeting Request',
                       card_title="Information", form=form,
                       meeting_ul='menu-open'
                       )
        return render(request, 'meeting/meeting_request_form.html', context=context)
    else:
        form = Meeting_Form(request.POST)
        is_valid = form.is_valid()
        is_meeting_start_time_valid = True
        is_meeting_end_time_valid = True
        meeting_valid = True
        t_end_time = datetime.now().time()

        if is_valid:
            t_date = form.cleaned_data['date']
            t_day = get_weekday_from_date(t_date)
            t_start_time = form.cleaned_data['start_time']
            t_duration = form.cleaned_data['meeting_duration']
            t_end_time = add_time(t_start_time, t_duration)
            if not is_valid_meeting_time(t_start_time, t_day, faculty):
                is_meeting_start_time_valid = False
                form.add_time__error()
            if not is_valid_meeting_time(t_end_time, t_day, faculty):
                is_meeting_end_time_valid = False
                form.add_duration__error()
            if not (is_meeting_end_time_valid and is_meeting_start_time_valid):
                form.add_date_error()
            if not is_valid_meeting_time_check_between(t_start_time, t_end_time, t_day, faculty):
                is_meeting_end_time_valid = False
                is_meeting_start_time_valid = False
                form.add_duration__error()
                form.add_time__error()
                messages.error(request,
                               f'{faculty.first_name} has some other schedules between {t_start_time.strftime("%H:%M")} and {t_end_time.strftime("%H:%M")}')
            if not is_valid_meeting(t_start_time, t_end_time, t_date, faculty):
                form.add_invalid_meeting_faculty()
                meeting_valid = False
            if not is_valid_meeting_requester(t_start_time, t_end_time, t_date, request.user):
                form.add_invalid_meeting_user()
                meeting_valid = False
        if is_valid and is_meeting_start_time_valid and is_meeting_end_time_valid and meeting_valid:
            messages.info(request, 'meeting added')
            meeting = form.save(commit=False)
            detail_form = Meeting_Detail_Form(request.POST)
            meeting_detail = detail_form.save(commit=False)
            role = request.session.get('login_role', 'None')
            if role == 'faculty':
                meeting.requester_type = 'f'
            else:
                meeting.requester_type = 's'
            meeting_detail.owner_type = 'r'
            meeting.faculty = faculty
            meeting.user = request.user
            meeting.meeting_status = 'request'
            meeting_detail.meeting_status = 'request'
            meeting_detail.text = meeting.subject
            meeting.finish_time = t_end_time
            meeting.save()
            meeting_detail.meeting = meeting
            meeting_detail.save()
            notify.send(request.user, recipient=faculty.user, verb='You have Meeting new request')
            return redirect('meeting:meeting_request_user_view')
        else:
            messages.error(request, 'Correct the errors')
            context = dict(page_title='Administration-Meeting Request', h1_title='Meeting Request',
                           url='Meeting Request',
                           card_title="Information", form=form,
                           meeting_ul='menu-open'
                           )
            return render(request, 'meeting/meeting_request_form.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty', 'student'])
def meeting_approve(request, id):
    page = request.GET.get('next_page', 'None')
    if id <= 0:
        messages.error(request, 'Meeting Not found against this id')
        return my_redirect(page, id)
    else:
        try:
            meeting: Meeting = Meeting.objects.get(pk=id)
        except Meeting.DoesNotExist:
            messages.error(request, 'Meeting Not found against this id')
            return my_redirect(page, id)
    meeting_detail = Meeting_Detail()
    role = request.session.get('login_role', 'None')
    meeting_belongs_to_user = True
    if role == 'faculty':
        meeting_detail.owner_type = 'f'
        if meeting.requester_type == 'f':
            if meeting.user == request.user or meeting.faculty == request.user.faculty:
                if meeting.user == request.user:
                    meeting_detail.owner_type = 'r'
                else:
                    meeting_detail.owner_type = 'f'
            else:
                meeting_belongs_to_user = False
        else:
            if meeting.faculty != request.user.faculty:
                meeting_belongs_to_user = False
            meeting_detail.owner_type = 'f'
    elif role == 'student':
        if meeting.user != request.user:
            meeting_belongs_to_user = False
        meeting_detail.owner_type = 'r'
    else:
        meeting_belongs_to_user = False
    if meeting_belongs_to_user:
        meeting_detail.meeting = meeting
        meeting_detail.meeting_duration = meeting.meeting_duration
        meeting_detail.date = meeting.date
        meeting_detail.start_time = meeting.start_time
        meeting.meeting_status = 'approve'
        meeting_detail.meeting_status = 'approve'
        meeting_detail.text = f' Meeting Approved '
        meeting.save()
        meeting_detail.save()
        cancel_other_meetings_that_clash(meeting)
        messages.success(request, 'meeting approve')
    else:
        messages.error(request, 'Meeting Not found')
    return my_redirect(page, id)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty', 'student'])
def meeting_cancel(request, id):
    page = request.GET.get('next_page', 'None')
    if id <= 0:
        messages.error(request, 'Meeting Not found against this id')
        return my_redirect(page, id)
    else:
        try:
            meeting: Meeting = Meeting.objects.get(pk=id)
        except Meeting.DoesNotExist:
            messages.error(request, 'Meeting Not found against this id')
            return my_redirect(page, id)
    meeting_detail = Meeting_Detail()
    role = request.session.get('login_role', 'None')
    meeting_belongs_to_user = True
    if role == 'faculty':
        meeting_detail.owner_type = 'f'
        if meeting.requester_type == 'f':
            if meeting.user == request.user or meeting.faculty == request.user.faculty:
                if meeting.user == request.user:
                    meeting_detail.owner_type = 'r'
                else:
                    meeting_detail.owner_type = 'f'
            else:
                meeting_belongs_to_user = False
        else:
            if meeting.faculty != request.user.faculty:
                meeting_belongs_to_user = False
            meeting_detail.owner_type = 'f'
    elif role == 'student':
        if meeting.user != request.user:
            meeting_belongs_to_user = False
        meeting_detail.owner_type = 'r'
    if meeting_belongs_to_user:
        meeting_detail.meeting = meeting
        meeting.meeting_status = 'cancel'
        meeting_detail.meeting_status = 'cancel'
        meeting_detail.text = f' Meeting Canceled '
        meeting.save()
        meeting_detail.save()
        messages.success(request, 'meeting Canceled')
    else:
        messages.error(request, 'Meeting Not found')
    return my_redirect(page, id)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def meeting_reschedule(request, id):
    page = request.GET.get('next_page', 'None')
    if id <= 0:
        messages.error(request, 'Meeting Not found against this id')
        return my_redirect(page, id)
    else:
        try:
            meeting: Meeting = Meeting.objects.get(pk=id)
        except Meeting.DoesNotExist:
            messages.error(request, 'Meeting Not found against this id')
            return my_redirect(page, id)
    if meeting.faculty != request.user.faculty:
        messages.error(request, 'Can not rescheduled this meeting')
        return my_redirect(page, id)
    if request.method == 'GET':
        form = Meeting_Reschedule_Form(instance=meeting)
        context = dict(page_title='Administration-Meeting Reschedule', h1_title='Meeting Reschedule',
                       url='Meeting Reschedule',
                       card_title="Information", form=form,
                       meeting_ul='menu-open', d=meeting.date
                       )
        return render(request, 'meeting/meeting_reschedule_form.html', context=context)
    else:
        form = Meeting_Reschedule_Form(request.POST, instance=meeting)
        is_valid = form.is_valid()
        is_meeting_start_time_valid = True
        is_meeting_end_time_valid = True
        meeting_valid = True
        t_end_time = datetime.now().time()
        if is_valid:
            t_date = form.cleaned_data['date']
            t_day = get_weekday_from_date(t_date)
            t_start_time = form.cleaned_data['start_time']
            t_duration = form.cleaned_data['meeting_duration']
            t_end_time = add_time(t_start_time, t_duration)
            if not is_valid_meeting_time(t_start_time, t_day, meeting.faculty):
                is_meeting_start_time_valid = False
                form.add_time__error()
            if not is_valid_meeting_time(t_end_time, t_day, meeting.faculty):
                is_meeting_end_time_valid = False
                form.add_duration__error()
            if not is_valid_meeting_time_check_between(t_start_time, t_end_time, t_day, meeting.faculty):
                is_meeting_end_time_valid = False
                is_meeting_start_time_valid = False
                form.add_duration__error()
            if not (is_meeting_end_time_valid and is_meeting_start_time_valid):
                form.add_date_error()
            if not is_valid_meeting_update(t_start_time, t_end_time, t_date, meeting.faculty, meeting.id):
                form.add_invalid_meeting_faculty()
                meeting_valid = False
            if not is_valid_meeting_update_requester(t_start_time, t_end_time, t_date, meeting.user, meeting.id):
                form.add_invalid_meeting_user()
                meeting_valid = False
        if is_valid and is_meeting_start_time_valid and is_meeting_end_time_valid and meeting_valid:

            meeting = form.save(commit=False)
            detail_form = Meeting_Detail_Form(request.POST)
            meeting_detail = detail_form.save(commit=False)
            meeting_detail.owner_type = 'f'
            meeting.meeting_status = 're_scheduled'
            meeting_detail.meeting_status = 're_scheduled'
            meeting.finish_time = t_end_time
            meeting.save()
            meeting_detail.meeting = meeting
            meeting_detail.save()
            messages.success(request, 'meeting rescheduled')
            return my_redirect(page, id)
        else:
            messages.error(request, 'Check The Errors')
            context = dict(page_title='Administration-Meeting Reschedule', h1_title='Meeting Reschedule',
                           url='Meeting Reschedule',
                           card_title="Information", form=form,
                           meeting_ul='menu-open', next_page=page
                           )
            return render(request, 'meeting/meeting_reschedule_form.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty', 'student'])
def meeting_message(request, id):
    page = request.GET.get("next_page", 'index')
    if id <= 0:
        messages.error(request, 'Meeting Not found against this id')
        return my_redirect(page, id)
    else:
        try:
            meeting: Meeting = Meeting.objects.get(pk=id)
        except Meeting.DoesNotExist:
            messages.error(request, 'Meeting Not found against id')
            return my_redirect(page, id)
    if request.method == 'GET':
        messages.info(request, 'get method is not allow')
        return my_redirect(page, id)
    else:
        form = Meeting_Detail_Text_Form(request.POST)
        is_valid = form.is_valid()
        if is_valid:
            meeting_detail = form.save(commit=False)
            meeting_detail.owner_type = 'f'
            meeting_detail.meeting_status = 'message'
            role = request.session.get('login_role', 'None')
            meeting_belongs_to_user = True
            if role == 'faculty':
                meeting_detail.owner_type = 'f'
                if meeting.requester_type == 'f':
                    if meeting.user == request.user or meeting.faculty == request.user.faculty:
                        if meeting.user == request.user:
                            meeting_detail.owner_type = 'r'
                        else:
                            meeting_detail.owner_type = 'f'
                    else:
                        meeting_belongs_to_user = False
                else:
                    if meeting.faculty != request.user.faculty:
                        meeting_belongs_to_user = False
                    meeting_detail.owner_type = 'f'
            elif role == 'student':
                if meeting.user != request.user:
                    meeting_belongs_to_user = False
                meeting_detail.owner_type = 'r'
            else:
                meeting_belongs_to_user = False
            if meeting_belongs_to_user:
                meeting_detail.meeting = meeting
                meeting_detail.save()
                messages.info(request, 'message sent')
            else:
                messages.error(request, 'Meeting Not Found')
            print(f'page {page} id{id}')
            return my_redirect(page, id)
        else:
            messages.error(request, 'Check the error')

            context = dict(page_title='Administration-Meeting Message', h1_title='Meeting  Message',
                           url='Meeting  Message',
                           card_title="Information", form=form,
                           meeting_ul='menu-open', next_page=page, id=meeting.id,
                           )
            return render(request, 'meeting/meeting_request_message.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def meeting_request_view_faculty(request):
    faculty_q = Q(faculty=request.user.faculty)
    request_q = Q(meeting_status__icontains='request')
    meeting_reschedule_q = Q(meeting_status__icontains='re_scheduled')
    meeting_list = Meeting.objects.filter(faculty_q & (request_q | meeting_reschedule_q))
    context = dict(page_title='Meeting-Requests', h1_title='Meeting Requests', url='Meeting Request',
                   card_title="Meetings", meeting_list=meeting_list,
                   meeting_request_fa_li='active', meeting_fa_ul='menu-open', next_page='f_request'
                   )
    return render(request, 'meeting/meeting_request_view_faculty.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def meeting_reschedule_view_faculty(request):
    faculty_q = Q(faculty=request.user.faculty)
    meeting_reschedule_q = Q(meeting_status__icontains='re_scheduled')
    meeting_list = Meeting.objects.filter(faculty_q & meeting_reschedule_q)
    context = dict(page_title='Meeting-Reschedule', h1_title='Meeting Requests', url='Meeting Reschedule',
                   card_title="Meetings", meeting_list=meeting_list,
                   meeting_reschedule_fa_li='active', meeting_fa_ul='menu-open', next_page='f_reschedule'
                   )
    return render(request, 'meeting/meeting_reschedule_view_faculty.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def meeting_cancelled_view_faculty(request):
    faculty_q = Q(faculty=request.user.faculty)
    meeting_cancel_q = Q(meeting_status__icontains='cancel')
    meeting_system_cancel_q = Q(meeting_status__icontains='system_cancel')

    meeting_list = Meeting.objects.filter(faculty_q & (meeting_cancel_q | meeting_system_cancel_q))

    context = dict(page_title='Meeting-Cancel', h1_title='Meeting Requests', url='Meeting Cancel',
                   card_title="Meetings", meeting_list=meeting_list,
                   meeting_cancel_fa_li='active', meeting_fa_ul='menu-open', next_page='f_cancel'
                   )
    return render(request, 'meeting/meeting_cancelled_view_faculty.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def meeting_approve_view_faculty(request):
    faculty_q = Q(faculty=request.user.faculty)
    meeting_approve_q = Q(meeting_status__icontains='approve')

    meeting_list = Meeting.objects.filter(faculty_q & meeting_approve_q)

    context = dict(page_title='Meeting-Approve', h1_title='Meeting Approved', url='Meeting Approve',
                   card_title="Meetings", meeting_list=meeting_list,
                   meeting_approve_fa_li='active', meeting_fa_ul='menu-open', next_page='f_approve'
                   )
    return render(request, 'meeting/meeting_approve_view_faculty.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def meeting_complete_view_faculty(request):
    faculty_q = Q(faculty=request.user.faculty)
    meeting_complete_q = Q(meeting_status__icontains='complete')

    meeting_list = Meeting.objects.filter(faculty_q & meeting_complete_q)

    context = dict(page_title='Meeting-Complete', h1_title='Meeting Complete', url='Meeting Complete',
                   card_title="Meetings", meeting_list=meeting_list,
                   meeting_complete_fa_li='active', meeting_fa_ul='menu-open', next_page='f_complete'
                   )
    return render(request, 'meeting/meeting_complete_view_faculty.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def meeting_detail_view_faculty(request, id):
    page = request.GET.get("next_page", 'index')
    if id <= 0:
        messages.error(request, 'Meeting Not found against this id')
        return my_redirect(page, id)
    else:
        try:
            meeting: Meeting = Meeting.objects.get(pk=id)
        except Meeting.DoesNotExist:
            messages.error(request, 'Meeting Not found against this id')
            return my_redirect(page, id)
    meeting_belongs_to_user = True
    if meeting.faculty != request.user.faculty:
        meeting_belongs_to_user = False
        messages.info(request, 'meeting not found')
    if meeting_belongs_to_user:
        meeting_detail_list = meeting.meeting_detail_set.all().order_by('initiate_time')
        form = Meeting_Reschedule_Form(instance=meeting)
        mform = Meeting_Detail_Text_Form()
        context = dict(page_title='Meeting-Detail', h1_title='Meeting Detail', url='Meeting detail',
                       meeting=meeting, meeting_detail_list=meeting_detail_list, form=form, mform=mform,
                       meeting_fa_ul='menu-open', next_page='f_da'
                       )
        return render(request, 'meeting/meeting_detail_view.html', context=context)
    else:
        return my_redirect(page, id)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty'])
def meeting_complete(request, id):
    page = request.GET.get("next_page", 'index')
    if id <= 0:
        messages.error(request, 'Meeting Not found against this id')
        return my_redirect(page, id)
    else:
        try:
            meeting: Meeting = Meeting.objects.get(pk=id)
        except Meeting.DoesNotExist:
            messages.error(request, 'Meeting Not found against id or In-Valid id')
            return my_redirect(page, id)
    meeting_belongs_to_user = True
    if meeting.faculty != request.user.faculty:
        meeting_belongs_to_user = False
        messages.info(request, 'meeting not found')
    if meeting_belongs_to_user:
        meeting_detail = Meeting_Detail()
        meeting_detail.meeting = meeting
        meeting.meeting_status = 'complete'
        meeting_detail.meeting_status = 'complete'
        meeting_detail.text = f' Meeting Conducted'
        meeting.save()
        meeting_detail.save()
        messages.success(request, 'Meeting marked as completed')
    else:
        messages.error(request, 'something went wrong')
    return my_redirect(page, id)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['faculty', 'student'])
def meeting_detail_view_requester(request, id):
    page = request.GET.get("next_page", 'index')
    if id <= 0:
        messages.error(request, 'Meeting Not found against this id')
        return my_redirect(page, id)
    else:
        try:
            meeting: Meeting = Meeting.objects.get(pk=id)
        except Meeting.DoesNotExist:
            messages.error(request, 'Meeting Not found against this id')
            return my_redirect(page, id)
    role = request.session.get('login_role', 'None')
    meeting_belongs_to_user = True
    if role == 'faculty':
        if meeting.requester_type == 'f':
            if meeting.user != request.user:
                meeting_belongs_to_user = False
    elif role == 'student':
        if meeting.user != request.user:
            meeting_belongs_to_user = False
    else:
        meeting_belongs_to_user = False

    meeting_detail_list = meeting.meeting_detail_set.all().order_by('initiate_time')
    if meeting_belongs_to_user:
        mform = Meeting_Detail_Text_Form()
        context = dict(page_title='Meeting-Detail', h1_title='Meeting Detail', url='Meeting detail',
                       meeting=meeting, meeting_detail_list=meeting_detail_list, mform=mform,
                       meeting_fa_ul='menu-open', next_page='r_da'
                       )
        return render(request, 'meeting/meeting_detail_requester_view.html', context=context)
    else:
        return my_redirect(page, id)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['student', 'faculty'])
def meeting_request_view_user(request):
    user_q = Q(user=request.user)
    request_q = Q(meeting_status__icontains='request')
    meeting_list = Meeting.objects.filter(user_q & request_q)
    context = dict(page_title='Meeting-Requests', h1_title='Meeting Requests', url='Meeting Request',
                   card_title="Meetings", meeting_list=meeting_list,
                   meeting_request_ra_li='active', meeting_ra_ul='menu-open', next_page='r_request'
                   )
    return render(request, 'meeting/meeting_request_view_user.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['student', 'faculty'])
def meeting_complete_view_user(request):
    user_q = Q(user=request.user)

    meeting_complete_q = Q(meeting_status__icontains='complete')
    meeting_list = Meeting.objects.filter(user_q & meeting_complete_q)
    context = dict(page_title='Meeting-Complete', h1_title='Meeting Complete', url='Meeting Complete',
                   card_title="Meetings", meeting_list=meeting_list,
                   meeting_complete_ra_li='active', meeting_ra_ul='menu-open', next_page='r_complete'
                   )
    return render(request, 'meeting/meeting_complete_view_user.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['student', 'faculty'])
def meeting_reschedule_view_user(request):
    user_q = Q(user=request.user)
    meeting_reschedule_q = Q(meeting_status__icontains='re_scheduled')
    meeting_list = Meeting.objects.filter(user_q & meeting_reschedule_q)
    context = dict(page_title='Meeting-Reschedule', h1_title='Meeting Requests', url='Meeting Reschedule',
                   card_title="Meetings", meeting_list=meeting_list,
                   meeting_reschedule_ra_li='active', meeting_ra_ul='menu-open', next_page='r_reschedule'
                   )
    return render(request, 'meeting/meeting_reschedule_view_user.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['student', 'faculty'])
def meeting_cancelled_view_user(request):
    user_q = Q(user=request.user)
    meeting_cancel_q = Q(meeting_status__icontains='cancel')
    meeting_system_cancel_q = Q(meeting_status__icontains='system_cancel')

    meeting_list = Meeting.objects.filter(user_q & (meeting_cancel_q | meeting_system_cancel_q))

    context = dict(page_title='Meeting-Cancel', h1_title='Meeting Requests', url='Meeting Cancel',
                   card_title="Meetings", meeting_list=meeting_list,
                   meeting_cancel_ra_li='active', meeting_ra_ul='menu-open', next_page='r_cancelled'
                   )
    return render(request, 'meeting/meeting_cancelled_view_user.html', context=context)


@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['student', 'faculty'])
def meeting_approve_view_user(request):
    user_q = Q(user=request.user)
    meeting_approve_q = Q(meeting_status__icontains='approve')

    meeting_list = Meeting.objects.filter(user_q & meeting_approve_q)

    context = dict(page_title='Meeting-Approve', h1_title='Meeting Approved', url='Meeting Approve',
                   card_title="Meetings", meeting_list=meeting_list,
                   meeting_approve_ra_li='active', meeting_ra_ul='menu-open', next_page='r_approve',
                   )
    return render(request, 'meeting/meeting_approve_view_user.html', context=context)


def my_redirect(page, id):
    if page == 'f_request':
        return redirect('meeting:meeting_request_faculty_view')
    elif page == 'f_approve':
        return redirect('meeting:meeting_approve_faculty_view')
    elif page == 'f_cancel':
        return redirect('meeting:meeting_cancel_faculty_view')
    elif page == 'f_reschedule':
        return redirect('meeting:meeting_reschedule_faculty_view')
    elif page == 'f_complete':
        return redirect('meeting:meeting_complete_faculty_view')
    elif page == 'r_request':
        return redirect('meeting:meeting_request_user_view')
    elif page == 'r_approve':
        return redirect('meeting:meeting_approve_user_view')
    elif page == 'r_cancel':
        return redirect('meeting:meeting_cancel_user_view')
    elif page == 'r_reschedule':
        return redirect('meeting:meeting_reschedule_user_view')
    elif page == 'r_complete':
        return redirect('meeting:meeting_complete_user_view')
    elif page == 'f_da':
        return redirect('meeting:meeting_detail_faculty_view', id)
    elif page == 'r_da':
        return redirect('meeting:meeting_detail_requester_view', id)
    return redirect('faculty:all_available_faculty_sidebar')
