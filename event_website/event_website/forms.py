from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User, Event

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'full_name')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name')

class SignupForm(forms.Form):
    full_name = forms.CharField(max_length=100, label='Full Name')

    def signup(self, request, user):
        user.full_name = self.cleaned_data['full_name']
        user.save()

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