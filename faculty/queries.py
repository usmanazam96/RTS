from faculty.models import *
from django.db.models import Q
from meeting.models import Meeting


def is_valid_schedule_time(time, day, faculty):
    start_time_q = Q(start_time__lte=time)
    end_time_q = Q(end_time__gte=time)
    day_q = Q(day__exact=day)
    faculty_q = Q(faculty=faculty)
    count = Schedule.objects.filter(start_time_q & end_time_q & day_q & faculty_q).count()
    if count > 0:
        return False
    return True


def is_valid_schedule_time_id(time, day, faculty, id):
    start_time_q = Q(start_time__lte=time)
    end_time_q = Q(end_time__gte=time)
    day_q = Q(day__exact=day)
    faculty_q = Q(faculty=faculty)
    id_q = Q(id=id)
    count = Schedule.objects.filter(start_time_q & end_time_q & day_q & faculty_q & ~id_q).count()
    if count > 0:
        return False
    return True


def is_valid_schedule_time_check_between(start_time, end_time, day, faculty):
    start_time_q = Q(start_time__range=(start_time, end_time))
    end_time_q = Q(end_time__range=(start_time, end_time))
    day_q = Q(day__exact=day)
    faculty_q = Q(faculty=faculty)
    count = Schedule.objects.filter((start_time_q | end_time_q) & day_q & faculty_q).count()
    if count > 0:
        return False
    return True


def is_valid_schedule_time_check_between_id(start_time, end_time, day, faculty, id):
    start_time_q = Q(start_time__range=(start_time, end_time))
    end_time_q = Q(end_time__range=(start_time, end_time))
    day_q = Q(day__exact=day)
    faculty_q = Q(faculty=faculty)
    id_q = Q(id=id)
    count = Schedule.objects.filter((start_time_q | end_time_q) & day_q & faculty_q & ~id_q).count()
    if count > 0:
        return False
    return True


def dashboard(faculty):
    faculty_q = Q(faculty=faculty)
    meeting_reschedule_q = Q(meeting_status__icontains='re_scheduled')
    meeting_cancel_q = Q(meeting_status__icontains='cancel')
    meeting_approve_q = Q(meeting_status__icontains='approve')
    meeting_complete_q = Q(meeting_status__icontains='complete')
    meeting_system_cancel_q = Q(meeting_status__icontains='system_cancel')
    meeting_request_q = Q(meeting_status__icontains='request')
    count_meeting_requests = Meeting.objects.filter(faculty_q & meeting_request_q).count()
    count_meeting_reschedule = Meeting.objects.filter(faculty_q & meeting_reschedule_q).count()
    count_meeting_approve = Meeting.objects.filter(faculty_q & meeting_approve_q).count()
    count_meeting_complete = Meeting.objects.filter(faculty_q & meeting_complete_q).count()
    count_meeting_cancel = Meeting.objects.filter(faculty_q & (meeting_system_cancel_q | meeting_cancel_q)).count()
    data = dict(count_meeting_approve=count_meeting_approve, count_meeting_complete=count_meeting_complete,
                count_meeting_reschedule=count_meeting_reschedule, count_meeting_requests=count_meeting_requests,
                count_meeting_cancel=count_meeting_cancel)
    return data
