from django import forms
from meeting.models import *
from meeting.functions import *


class Meeting_Form(forms.ModelForm):
    class Meta:
        model = Meeting
        exclude = ['user', 'faculty', 'meeting_status', 'requester_type', 'initiate_time', 'finish_time']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            t_date = cleaned_data["date"]
            t_days = 0
            if not is_future_date(t_date, t_days):
                self.add_error('date', f'meeting should be in future with {t_days} day')
        return cleaned_data

    def add_date_error(self):
        self.add_error('date', f'meeting date day and time clash with faculty schedule')

    def add_time__error(self):
        self.add_error('start_time', f'meeting time clash with faculty schedule')

    def add_duration__error(self):
        self.add_error('meeting_duration', f'meeting end time clash with faculty schedule')

    def add_invalid_meeting_faculty(self):
        self.add_error('date', f'meeting date clash with faculty meetings')
        self.add_error('start_time', f'meeting time clash with faculty meetings')
        self.add_error('meeting_duration', f'meeting end time clash with faculty meetings')

    def add_invalid_meeting_user(self):
        self.add_error('date', f'meeting date clash with your meetings')
        self.add_error('start_time', f'meeting time clash with your meetings')
        self.add_error('meeting_duration', f'meeting end time clash with yours meetings')


class Meeting_Reschedule_Form(forms.ModelForm):
    class Meta:
        model = Meeting
        exclude = ['user', 'faculty', 'meeting_status', 'requester_type', 'initiate_time', 'finish_time', 'subject']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            t_date = cleaned_data["date"]
            t_days = 0
            if not is_future_date(t_date, t_days):
                self.add_error('date', f'meeting should be in future with {t_days} day')
        return cleaned_data

    def add_date_error(self):
        self.add_error('date', f'meeting date day and time clash with faculty schedule')

    def add_time__error(self):
        self.add_error('start_time', f'meeting time clash with faculty schedule')

    def add_duration__error(self):
        self.add_error('meeting_duration', f'meeting end time clash with faculty schedule')

    def add_invalid_meeting_faculty(self):
        self.add_error('date', f'meeting date clash with faculty meetings')
        self.add_error('start_time', f'meeting time clash with faculty meetings')
        self.add_error('meeting_duration', f'meeting end time clash with faculty meetings')

    def add_invalid_meeting_user(self):
        self.add_error('date', f'meeting date clash with your meetings')
        self.add_error('start_time', f'meeting time clash with your meetings')
        self.add_error('meeting_duration', f'meeting end time clash with yours meetings')


class Meeting_Detail_Text_Form(forms.ModelForm):
    text = forms.CharField(max_length=255, required=True)

    class Meta:
        model = Meeting_Detail
        fields = ['text']
        labels = {
            "text": "Embed"
        }


class Meeting_Detail_Text_Form_Empty_Allow(forms.ModelForm):
    class Meta:
        model = Meeting_Detail
        fields = ['text']
        labels = {'text': "Message"}


class Meeting_Detail_Form(forms.ModelForm):
    class Meta:
        model = Meeting_Detail
        fields = ['date', 'start_time', 'meeting_duration']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data:
            t_date = cleaned_data["date"]
            t_days = 0
            if not is_future_date(t_date, t_days):
                self.add_error('date', f'meeting should be in future with {t_days} day')
        return cleaned_data

    def add_date_error(self):
        self.add_error('date', f'meeting date day and time clash with faculty schedule')

    def add_time__error(self):
        self.add_error('start_time', f'meeting time clash with faculty schedule')

    def add_duration__error(self):
        self.add_error('meeting_duration', f'meeting end time clash with faculty schedule')

    def add_invalid_meeting_faculty(self):
        self.add_error('date', f'meeting date clash with faculty meetings')
        self.add_error('start_time', f'meeting time clash with faculty meetings')
        self.add_error('meeting_duration', f'meeting end time clash with faculty meetings')

    def add_invalid_meeting_user(self):
        self.add_error('date', f'meeting date clash with your meetings')
        self.add_error('start_time', f'meeting time clash with your meetings')
        self.add_error('meeting_duration', f'meeting end time clash with yours meetings')
