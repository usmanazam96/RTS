from django.db import models
from accounts.models import *

# Create your models here.
'''
class Meeting(models.Model):
    status_choice = (
        ('P', 'Pending'),
        ('A', 'Approve'),
        ('PP', 'Post Poned'),
        ('C', 'Canceled'),
    )
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    studentId = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_time=models.DateTimeField()
    meeting_duration = models.IntegerField()
    meeting_status=models.CharField(max_length=2, choices=status_choice)

'''
