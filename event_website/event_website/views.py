from django.shortcuts import render, redirect
from django.contrib import messages
import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Event, AppUser
from .forms import EventCreateForm, CustomUserCreationForm

def home(request, filter_result = None):
    # if no filter result, return all events with finishing date from today onwards
    if not filter_result: 
        events = Event.objects.filter(finish_date__gte=datetime.date.today()).order_by('-finish_date')
        context = { 'events': events }
    else:
        context = filter_result
    return render(request, 'home.html', context)

def filter_view(request):
    if request.method == 'GET':
        try: # Try converting the date input. Will fail with an invalid date.
            start_filter = datetime.datetime.strptime(request.GET.get("start_filter"), '%Y-%m-%d')
            finish_filter = datetime.datetime.strptime(request.GET.get("finish_filter"),  '%Y-%m-%d')
        except ValueError:
            messages.info(request, "Please check your filter dates.")
            return redirect('home')

        # Make sure both start and finishing dates exists and are valid.
        if start_filter and finish_filter and (finish_filter >= start_filter):
            # Find events that starts after the start filter and finishes before the finish filter
            events = Event.objects.filter(finish_date__lte=finish_filter).filter(start_date__gte=start_filter).order_by('finish_date')
            filter_result = {
                'start_filter': start_filter,
                'finish_filter': finish_filter,
                'events': events
            }
            return home(request, filter_result=filter_result)
        messages.info(request, "Please check your filter dates.")
        return redirect('home')
    request.messages(request, "You've taken a wrong turn.")
    return redirect('home')



@login_required
def event_create_view(request):
    # Create event using the model form
    form = EventCreateForm(request.POST or None)
    if form.is_valid():
        event = form.save(commit=False)
        event.created_by = request.user # Add metadata on which user created the event
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
        if event.created_by.id != user_id: # Make sure creator cannot attend their own event
            user = AppUser.objects.get(pk=user_id)
            event.users_attending.add(user)
            event.save()
            messages.info(request,"You have successfully attended {}".format(event.name))
            return redirect('home')
        else:
            messages.info(request, "You cannot attend events you have created.")
            return redirect('home')
    request.messages(request, "You've taken a wrong turn.")
    return redirect('home')