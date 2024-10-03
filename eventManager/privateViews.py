from django.contrib.auth import authenticate, login, logout
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages


from . import settings
from .forms import  AddEventForm


def adminLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Get the JWT token after successful login
            response = requests.post(f"{settings.BASE_API_URL}/api/token/",
                                     json={'username': username, 'password': password})
            if response.status_code == 200:
                tokens = response.json()
                request.session["access_token"] = tokens['access']
                request.session["refresh_token"] = tokens['refresh']
            login(request, user)
            return redirect('/events/')  # Redirect to the home page or another view
        else:
            # Return an 'invalid login' error message
            messages.error(request, 'Invalid username or password')
            return redirect('/login/')  # Redirect back to login page
    else:
        return render(request, 'login.html')  # Display the login page

def adminLogout(request):
    logout(request)
    if 'access_token' in request.session:
        del request.session['access_token']
    if 'refresh_token' in request.session:
        del request.session['refresh_token']

    messages.success(request, "successfully logged out")
    return redirect('home')



@login_required
def addEvent(request):
    if request.method == "POST":
        form = AddEventForm(request.POST)
        if form.is_valid():
            # Prepare the data to send to the API
            data = {
                "title": form.cleaned_data["title"],
                "start_date": form.cleaned_data["start_date"].isoformat(),  # Convert to ISO format if needed
                "end_date": form.cleaned_data["end_date"].isoformat(),      # Convert to ISO format if needed
                "thumbnail": form.cleaned_data.get("thumbnail", None)       # Assuming you have a thumbnail field
            }
            access_token = request.session["access_token"]
            # Check if the access token is available
            if not access_token:
                # Handle the case where the token is missing (e.g., redirect to login or show error)
                messages.success(request, "Access Denied")
                return redirect("home")

            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            # Send the POST request to your API endpoint
            response = requests.post(f"{settings.BASE_API_URL}/api/addEvent/", headers = headers, json=data)

            if response.status_code == 201:  # Event created successfully
                messages.error(request, "event created successfully")
                return redirect("home")
        else:
            messages.error(request, "can not create an event be carefull with dates it may be incorrect")


    form = AddEventForm()
    return render(request, "add_event.html", {'form': form})

@login_required()
def deleteEvent(request, pk):
    if request.method == "POST":
        access_token = request.session["access_token"]
        # Check if the access token is available
        if not access_token:
            # Handle the case where the token is missing (e.g., redirect to login or show error)
            messages.success(request, "Access Denied")
            return redirect("home")


        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.delete(url = f"{settings.BASE_API_URL}/api/deleteEvent/{pk}/", headers= headers)

        if response.status_code == 200:  # Event created successfully
            messages.success(request, "event deleted successfully")
            return redirect("home")
        else:
            # error
            messages.error(request, "can not delete an event")
            return redirect("home")

    return redirect("home")