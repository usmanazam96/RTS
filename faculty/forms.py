from django import forms
from faculty.models import *


class FacultyAvailabilityForm(forms.ModelForm):
    class Meta:
        model = FacultyAvailability
        exclude = ['faculty']
