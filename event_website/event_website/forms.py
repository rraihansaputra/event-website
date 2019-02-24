from django import forms

from .models import Event

class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'start_date',
            'finish_date',
            'details',
        ]
        widgets = {
            'start_date': forms.DateInput,
            'finish_date': forms.DateInput,
        }