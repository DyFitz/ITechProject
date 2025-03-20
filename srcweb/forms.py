from django import forms
from .models import Event

# Form class linked to the Event model
class EventForm(forms.ModelForm):
    class Meta:
        model = Event # Specifies which model the form corresponds to
        # Fields to include in the form
        fields = ['title', 'description', 'event_date', 'location', 'total_tickets']