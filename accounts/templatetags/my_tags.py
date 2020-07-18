from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='show_approve')
def show_approve(meeting_detail):
    meeting = meeting_detail.meeting
    if ((meeting.date == meeting_detail.date and meeting.start_time == meeting_detail.start_time and
         meeting.meeting_duration == meeting_detail.meeting_duration) and (
            meeting.meeting_status == 'request' or meeting.meeting_status == 're_scheduled')):
        return True
    else:
        return False
