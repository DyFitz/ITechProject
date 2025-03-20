from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from .models import Event
from .forms import EventForm


def home(request):
    return render(request, 'srcweb/home.html')

def events(request):
    events_list = Event.objects.all()
    return render(request, 'srcweb/events.html', {'events': events_list})

def eventdetails_student(request):
    return render(request, 'srcweb/eventdetails_student.html')
def eventdetails_staff(request):
    return render(request, 'srcweb/eventdetails_staff.html')

def myaccount(request):
    return render(request, 'srcweb/myaccount.html')

def dancingsociety(request):
    return render(request, 'srcweb/dancingsociety.html')


# Allows users with add event permission to create events
@permission_required('srcweb.add_event', raise_exception=True)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.available_tickets = event.total_tickets
            event.save()
            return redirect('srcweb:events')
    else:
        form = EventForm()
    return render(request, 'srcweb/create_event.html', {'form': form})