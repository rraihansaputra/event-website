from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Event
from .forms import EventCreateForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
    #TODO add user email to sign up
    #TODO add user full name to sign up (use email as username?)

def home(request):
    print(request.user)
    events = Event.objects.all().order_by('-created_time')
    return render(request, 'home.html', {'events': events})
    #TODO add login button if not logged in
    #TODO change query to have events from today forward only

def event_create_view(request):
    form = EventCreateForm(request.POST or None)
    if form.is_valid():
        event = form.save(commit=False)
        event.created_by = request.user
        event.save()
        return redirect('home')
    return render(request,'create_event.html', {'form': form})
    #TODO require login
    #TODO restrict date to future

def event_attend_view(request):
    if request.method == 'POST':
        user_id = request.user.id
        event_id = request.POST.get("event_id")
        print(event_id)
        event = Event.objects.get(pk=event_id)
        user = User.objects.get(pk=user_id)
        print(user)
        event.users_attending.add(user)
        print(event.users_attending.all())
        event.save()
        print(event.users_attending.all())
        return redirect(home)
    #TODO handle these cases:
    #   what to do when event creator attends an event -> need to fail
    #   how to handled attended event (handle on template?)
    #TODO require login