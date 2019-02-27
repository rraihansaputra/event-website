from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import AppUser, Event

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = AppUser
        fields = ('username', 'email', 'full_name')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = AppUser
        fields = ('username', 'email', 'full_name')

class SignupForm(forms.Form):
    # add field to have the full name on the signup page
    full_name = forms.CharField(max_length=100, label='Full Name')

    def signup(self, request, user):
        user.full_name = self.cleaned_data['full_name']
        user.save()

class EventCreateForm(forms.ModelForm):

    def clean(self):
        # Override the ModelForm clean function to make sure finish date is >= start date
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        finish_date = cleaned_data.get('finish_date')

        if finish_date and start_date and (finish_date < start_date):
            raise forms.ValidationError(
                "Event finish date must be equal or later than the event start date"
            )

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
