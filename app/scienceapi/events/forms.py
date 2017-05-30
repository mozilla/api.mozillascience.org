from django import forms
import pytz


ALL_TIMEZONES = [(i, i) for i in pytz.all_timezones]


class EventAdminForm(forms.ModelForm):
    timezone = forms.ChoiceField(choices=ALL_TIMEZONES)
