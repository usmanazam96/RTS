from faculty.models import *
from django.db.models import Q


def is_valid_schedule_time(time, day, faculty):
    start_time_q = Q(start_time__lte=time)
    end_time_q = Q(end_time__gte=time)
    day_q = Q(day__exact=day)
    faculty_q = Q(faculty=faculty)
    count = Schedule.objects.filter(start_time_q & end_time_q & day_q & faculty_q).count()
    if count > 0:
        return False
    return True


def is_valid_schedule_time(time, day, faculty, id):
    start_time_q = Q(start_time__lte=time)
    end_time_q = Q(end_time__gte=time)
    day_q = Q(day__exact=day)
    faculty_q = Q(faculty=faculty)
    id_q = Q(id=id)
    count = Schedule.objects.filter(start_time_q & end_time_q & day_q & faculty_q & ~id_q).count()
    if count > 0:
        return False
    return True
