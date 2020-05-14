from django.db import models
from accounts.models import Faculty


# Create your models here.
class FacultyAvailability(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    availability = models.BooleanField(default=False)
    availabilityMsg = models.TextField(blank=True, default="N/A")

    def __str__(self):
        return self.faculty.first_name 
'''
class ScheduleType(models.Model):
    type=models.CharField(max_length=30)
    type_description=models.CharField(max_length=255)
class  Schedule(models.Model):
    faculty=models.ForeignKey(Faculty,on_delete=models.CASCADE)
'''


