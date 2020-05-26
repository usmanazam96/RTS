import os

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
def content_file_faculty(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.first_name, instance.user.id, ext)
    return os.path.join('faculty_profile_pic', filename)


def content_file_student(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.first_name, instance.user.id, ext)
    return os.path.join('student_profile_pic', filename)


def content_file_admin(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.first_name, instance.user.id, ext)
    return os.path.join('admin_profile_pic', filename)


class Faculty(models.Model):
    gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    room_location = models.TextField(max_length=255)
    position = models.CharField(max_length=255, default='N/A')
    profile_pic = models.ImageField(upload_to=content_file_faculty, blank=True, null=True)
    gender = models.CharField(max_length=2, choices=gender_choice)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Student(models.Model):
    gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=30)
    profile_pic = models.ImageField(upload_to=content_file_student, null=True, blank=True)
    gender = models.CharField(max_length=2, choices=gender_choice)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Admin(models.Model):
    gender_choice = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to=content_file_admin, null=True, blank=True)
    gender = models.CharField(max_length=2, choices=gender_choice)

    def __str__(self):
        return self.first_name + " " + self.last_name
