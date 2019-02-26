from django.shortcuts import render, redirect
from django.contrib import messages
import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Event, User
from .forms import EventCreateForm, CustomUserCreationForm

def home(request):
    events = Event.objects.filter(finish_date__gte=datetime.date.today()).order_by('-created_time')
    return render(request, 'home.html', {'events': events})
    #TODO add login button if not logged in

@login_required
def event_create_view(request):
    form = EventCreateForm(request.POST or None)
    if form.is_valid():
        event = form.save(commit=False)
        event.created_by = request.user
        event.save()
        messages.info(request, "You have successfully created event {}".format(event.name))
        return redirect('home')
    return render(request,'create_event.html', {'form': form})

@login_required
def event_attend_view(request):
    if request.method == 'POST':
        user_id = request.user.id
        event_id = request.POST.get("event_id")
        event = Event.objects.get(pk=event_id)
        if event.created_by.id != user_id:
            user = User.objects.get(pk=user_id)
            event.users_attending.add(user)
            event.save()
            messages.info(request,"You have successfully attended {}".format(event.name))
            return home(request)
        else:
            messages.info(request, "You cannot attend events you have created.")
            return home(request)