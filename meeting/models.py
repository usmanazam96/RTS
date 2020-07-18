from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from accounts.models import *
from datetime import datetime


# Create your models here.

class Meeting(models.Model):
    status_choice = (
        ('approve', 'Approve'),
        ('cancel', 'Cancel'),
        ('re_scheduled', 'Re Schedule'),
        ('complete', 'Complete'),
        ('request', 'Request'),
        ('system_cancel', 'Canceled by System')
    )
    requester_type_choice = (
        ('s', 'Student'),
        ('f', 'faculty'),
    )
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    finish_time = models.TimeField(null=True)
    meeting_duration = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(180)],
                                           verbose_name='Duration (minute)')
    meeting_status = models.CharField(max_length=20, choices=status_choice)
    initiate_time = models.DateTimeField(default=datetime.now, blank=True)
    requester_type = models.CharField(max_length=2, choices=requester_type_choice)

    def __str__(self):
        return f'{self.id} {self.faculty} {self.date} {self.start_time} {self.meeting_duration} {self.finish_time} ' \
               f'{self.meeting_status} '


class Meeting_Detail(models.Model):
    status_choice = (
        ('message', 'message'),
        ('approve', 'Approve'),
        ('cancel', 'Cancel'),
        ('re_scheduled', 'Re Schedule'),
        ('complete', 'Complete'),
        ('request', 'Request'),
        ('system_cancel', 'Canceled by System')
    )
    type_choice = (
        ('r', 'requester'),
        ('f', 'faculty'),
        ('s', 'System')
    )
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
    meeting_duration = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(10)])
    meeting_status = models.CharField(max_length=20, choices=status_choice)
    initiate_time = models.DateTimeField(default=datetime.now, blank=True, null=True)
    owner_type = models.CharField(max_length=2, choices=type_choice)

    def __str__(self):
        return f" {self.meeting} {self.initiate_time}  {self.initiate_time} {self.owner_type}"
