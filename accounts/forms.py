from django import forms
from accounts.models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        exclude = ['user']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user']


class AdminForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user']
