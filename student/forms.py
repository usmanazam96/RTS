from django import forms
from accounts.models import *
from accounts.queries import *


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'student_id']
