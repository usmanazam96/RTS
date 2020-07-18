from django import forms
from django.core.exceptions import ValidationError

from faculty.models import *
from faculty.queries import is_valid_schedule_time
from faculty.functions import get_time_diff


class FacultyAvailabilityForm(forms.ModelForm):
    class Meta:
        model = FacultyAvailability
        exclude = ['faculty']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ['faculty']

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['schedule_type'].empty_label = '--- Please Select Type ---'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            start_time = cleaned_data["start_time"]
            end_time = cleaned_data['end_time']
            min_time = 15  # in minutes
            if get_time_diff(end_time, start_time) < min_time:
                self.add_error('end_time', f'end time should be greater than start time at least {min_time} minutes')
        return cleaned_data

    def add_start_time_clash_error(self):
        self.add_error('start_time', 'start time clash with other schedule time')

    def add_end_time_clash_error(self):
        self.add_error('end_time', 'end time clash with other schedule time')

    def add_in_valid_error(self):
        self.add_error('end_time', 'end time clash with other schedule time')
        self.add_error('start_time', 'start time clash with other schedule time')
