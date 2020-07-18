from django.db import models
from accounts.models import Faculty
from . import myFields
from django.utils.translation import ugettext as _
from datetime import datetime, date
from django.utils.timesince import timesince


# Create your models here.
class FacultyAvailability(models.Model):
    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE)
    availability = models.BooleanField(default=False)
    availabilityMsg = models.TextField(blank=True, default="Not Available")

    def __str__(self):
        return f'{self.faculty.first_name}  {self.availability}'


class ScheduleType(models.Model):
    type = models.CharField(max_length=30)
    type_description = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.type} '


class Schedule(models.Model):
    WEEKDAYS = [
        (None, ' --- Select Day --- '),
        (1, _(u"Monday")),
        (2, _(u"Tuesday")),
        (3, _(u"Wednesday")),
        (4, _(u"Thursday")),
        (5, _(u"Friday")),
        (6, _(u"Saturday")),
        (7, _(u"Sunday")),
    ]
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.IntegerField(
        choices=WEEKDAYS)
    schedule_type = models.ForeignKey(ScheduleType, on_delete=models.CASCADE)

    def get_time_diff(self):
        delta = datetime.combine(date.today(), self.end_time) - datetime.combine(date.today(), self.start_time)
        delta_minutes = (delta.days * 24 * 60 + delta.seconds) / 60
        if delta.days < 0:
            delta_minutes *= -1
        return delta_minutes

    def __str__(self):
        return f'{self.faculty.first_name}  {self.get_day_display()} start {self.start_time} end {self.end_time} '
