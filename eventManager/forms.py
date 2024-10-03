from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Event

class AddEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "start_date", "end_date", "thumbnail"]