from django import forms
from accounts.models import *
from accounts.queries import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data["email"]
        if self.instance.pk is None:  # insert
            if is_email_already_exist(email):
                self.add_error('email', 'email already exist')
        else:
            if is_email_already_exist_id(email, self.instance.pk):
                self.add_error('email', 'email already exist')

        return cleaned_data


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
        model = Admin
        exclude = ['user']
