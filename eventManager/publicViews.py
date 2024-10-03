from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import AddEventForm
from .models import Event
from django.conf import settings
import requests

def home(request):
    response = requests.get(f"{settings.BASE_API_URL}/api/events/")
    
    if response.status_code == 200:
        events = response.json()
    else:
        events = []  # In case of an error, returns an empty list
    
    # Pass the events data to the template
    return render(request, "events.html", {"events": events})


def event(request, pk):
    event = Event.objects.get(id=pk)
    return render(request, "event.html", {"event": event})



def events(request):
    events = Event.objects.all()
    return render(request, "events.html", {"events": events})

def registerOnEvent(request, pk):
    if f'event_{pk}_registered' in request.session:
        messages.error(request, "You have already registered for this event.")
        return redirect(f'/events/{pk}')

    try:
        response = requests.post(f"{settings.BASE_API_URL}/api/registerEvent/{pk}/")

        if response.status_code == 200:
            registration_code = response.json().get('code')
            messages.success(request, f"You have been registered. Your code is {registration_code} please save it:")
            request.session[f'event_{pk}_registered'] = True
        else:
            try:
                error_message = response.json().get('error', 'An unknown error occurred')
            except ValueError:
                error_message = 'An unknown error occurred while processing the response.'
            messages.error(request, f"Failed to register for the event. Error: {error_message}")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect(f'/events/{pk}')


def cancelRegistration(request, pk):
    if request.method == 'POST':
        confirmation_code = request.POST.get('confirmation_code')

        if not confirmation_code:
            messages.error(request, "Please provide a correct code")
            return redirect(f'/events/{pk}')
        try:
            response = requests.delete(f"{settings.BASE_API_URL}/api/cancelRegistration/{pk}/{confirmation_code}/")

            if response.status_code == 200:
                messages.success(request, "You have successfully canceled the event.")
                # Remove the session key when the registration is canceled
                if f'event_{pk}_registered' in request.session:
                    del request.session[f'event_{pk}_registered']
            else:
                try:
                    error_message = response.json().get('error', 'An unknown error occurred')
                except ValueError:
                    error_message = 'An unknown error occurred while processing the response.'
                messages.error(request, f"Failed to cancel the event. Error: {error_message}")

        except requests.exceptions.RequestException as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return redirect(f'/events/{pk}')



