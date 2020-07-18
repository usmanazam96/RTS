from faculty.models import *
from django.db.models import Q
from meeting.models import *


def is_valid_meeting_time(time, day, faculty):
    start_time_q = Q(start_time__lte=time)
    end_time_q = Q(end_time__gte=time)
    day_q = Q(day__exact=day)
    faculty_q = Q(faculty=faculty)
    type_q = Q(schedule_type__in=ScheduleType.objects.filter(type__icontains='lecture'))

    count = Schedule.objects.filter((start_time_q & end_time_q) & day_q & faculty_q & type_q).count()
    if count > 0:
        return False
    return True


def is_valid_meeting_time_check_between(start_time, end_time, day, faculty):
    start_time_q = Q(start_time__range=(start_time, end_time))
    end_time_q = Q(end_time__range=(start_time, end_time))
    day_q = Q(day__exact=day)
    faculty_q = Q(faculty=faculty)
    count = Schedule.objects.filter((start_time_q | end_time_q) & day_q & faculty_q).count()
    if count > 0:
        return False
    return True


def is_valid_meeting(start_time, t_finish_time, t_date, faculty):
    count = 0
    start_time_q = Q(start_time__lte=start_time)
    finish_time_q = Q(finish_time__gte=start_time)
    start_time_qf = Q(start_time__lte=t_finish_time)
    finish_time_qf = Q(finish_time__gte=t_finish_time)
    status_q = Q(meeting_status__icontains='approve')
    date_q = Q(date=t_date)
    faculty_q = Q(faculty=faculty)
    count = Meeting.objects.filter(
        ((start_time_q & finish_time_q) | (start_time_qf & finish_time_qf)) & date_q & faculty_q & status_q).count()
    if count > 0:
        return False
    return True


def is_valid_meeting_update(start_time, t_finish_time, date, faculty, id):
    count = 0
    start_time_q = Q(start_time__lte=start_time)
    finish_time_q = Q(finish_time__gte=start_time)
    start_time_qf = Q(start_time__lte=t_finish_time)
    finish_time_qf = Q(finish_time__gte=t_finish_time)
    date_q = Q(date=date)
    faculty_q = Q(faculty=faculty)
    id_q = Q(id=id)
    status_q = Q(meeting_status__icontains='approve')
    count = Meeting.objects.filter(
        ((start_time_q & finish_time_q) | (
                start_time_qf & finish_time_qf)) & date_q & faculty_q & ~id_q & status_q).count()
    if count > 0:
        return False
    return True


def is_valid_meeting(start_time, t_finish_time, t_date, faculty):
    count = 0
    start_time_q = Q(start_time__lte=start_time)
    finish_time_q = Q(finish_time__gte=start_time)
    start_time_qf = Q(start_time__lte=t_finish_time)
    finish_time_qf = Q(finish_time__gte=t_finish_time)
    date_q = Q(date=t_date)
    faculty_q = Q(faculty=faculty)
    status_q = Q(meeting_status__icontains='approve')
    count = Meeting.objects.filter(
        ((start_time_q & finish_time_q) | (start_time_qf & finish_time_qf)) & date_q & faculty_q & status_q).count()
    if count > 0:
        return False
    return True


def is_valid_meeting_update(start_time, t_finish_time, t_date, faculty, id):
    count = 0
    start_time_q = Q(start_time__lte=start_time)
    finish_time_q = Q(finish_time__gte=start_time)
    start_time_qf = Q(start_time__lte=t_finish_time)
    finish_time_qf = Q(finish_time__gte=t_finish_time)
    date_q = Q(date=t_date)
    faculty_q = Q(faculty=faculty)
    id_q = Q(id=id)
    status_q = Q(meeting_status__icontains='approve')
    count = Meeting.objects.filter(
        ((start_time_q & finish_time_q) | (start_time_qf & finish_time_qf)) & date_q & faculty_q & ~id_q & status_q
    ).count()
    if count > 0:
        return False
    return True


def is_valid_meeting_requester(start_time, t_finish_time, t_date, user):
    count = 0
    start_time_q = Q(start_time__lte=start_time)
    finish_time_q = Q(finish_time__gte=start_time)
    start_time_qf = Q(start_time__lte=t_finish_time)
    finish_time_qf = Q(finish_time__gte=t_finish_time)
    date_q = Q(date=t_date)
    user_q = Q(user=user)
    status_q = Q(meeting_status__icontains='approve')
    count = Meeting.objects.filter(
        ((start_time_q & finish_time_q) | (start_time_qf & finish_time_qf)) & date_q & user_q & status_q).count()
    if count > 0:
        return False
    return True


def is_valid_meeting_update_requester(start_time, t_finish_time, t_date, user, id):
    count = 0
    start_time_q = Q(start_time__lte=start_time)
    finish_time_q = Q(finish_time__gte=start_time)
    start_time_qf = Q(start_time__lte=t_finish_time)
    finish_time_qf = Q(finish_time__gte=t_finish_time)
    date_q = Q(date=t_date)
    user_q = Q(user=user)
    id_q = Q(id=id)
    status_q = Q(meeting_status__icontains='approve')
    count = Meeting.objects.filter(
        ((start_time_q & finish_time_q) | (
                start_time_qf & finish_time_qf)) & date_q & user_q & ~id_q & status_q).count()
    if count > 0:
        return False
    return True


def cancel_other_meetings_that_clash(meeting):
    start_time_q = Q(start_time__lte=meeting.start_time)
    finish_time_q = Q(finish_time__gte=meeting.start_time)
    start_time_qf = Q(start_time__lte=meeting.finish_time)
    finish_time_qf = Q(finish_time__gte=meeting.finish_time)
    date_q = Q(date=meeting.date)
    user_q = Q(user=meeting.user)
    faculty_q = Q(faculty=meeting.faculty)
    status_q = Q(meeting_status__icontains='approve')
    status_cq = Q(meeting_status__icontains='complete')
    id_q = Q(id=meeting.id)
    Meeting.objects.filter(
        ((start_time_q & finish_time_q) | (start_time_qf & finish_time_qf)) & date_q & (
                faculty_q | user_q) & ~id_q & ~status_q & ~status_cq).update(
        meeting_status='system_cancel')
    meetings = Meeting.objects.filter(
        ((start_time_q & finish_time_q) | (start_time_qf & finish_time_qf)) & date_q & (
                faculty_q | user_q) & ~id_q & ~status_q, ~status_cq)
    meeting_detail = Meeting_Detail()
    meeting_detail.meeting_status = 'system_cancel'
    meeting_detail.owner_type = 's'
    meeting_detail.text = "Meeting Cancelled By System due to another meeting is scheduled at that time and day"
    for m in meetings:
        meeting_detail.id = None
        meeting_detail.meeting = m
        meeting_detail.save()
