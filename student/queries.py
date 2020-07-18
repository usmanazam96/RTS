from django.db.models import Q
from meeting.models import Meeting


def dashboard(student):
    user_q = Q(user__student=student)
    meeting_reschedule_q = Q(meeting_status__icontains='re_scheduled')
    meeting_cancel_q = Q(meeting_status__icontains='cancel')
    meeting_approve_q = Q(meeting_status__icontains='approve')
    meeting_complete_q = Q(meeting_status__icontains='complete')
    meeting_system_cancel_q = Q(meeting_status__icontains='system_cancel')
    meeting_request_q = Q(meeting_status__icontains='request')
    count_meeting_requests = Meeting.objects.filter(user_q & meeting_request_q).count()
    count_meeting_reschedule = Meeting.objects.filter(user_q & meeting_reschedule_q).count()
    count_meeting_approve = Meeting.objects.filter(user_q & meeting_approve_q).count()
    count_meeting_complete = Meeting.objects.filter(user_q & meeting_complete_q).count()
    count_meeting_cancel = Meeting.objects.filter(user_q & (meeting_system_cancel_q | meeting_cancel_q)).count()
    data = dict(count_meeting_approve=count_meeting_approve, count_meeting_complete=count_meeting_complete,
                count_meeting_reschedule=count_meeting_reschedule, count_meeting_requests=count_meeting_requests,
                count_meeting_cancel=count_meeting_cancel)
    return data
