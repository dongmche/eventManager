from django.contrib import admin
from django.urls import path, include
from . import publicViews, privateViews
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



urlpatterns = [
    # integrate with api
    path('api/', include('api.apiUrls')),

    # public endpoints
    path('', publicViews.home, name="home"),
    path('events/', publicViews.events, name="events"),
    path('events/<int:pk>', publicViews.event, name="event"),
    path('register/<int:pk>/', publicViews.registerOnEvent, name="event"),
    path('cancelRegistration/<int:pk>/', publicViews.cancelRegistration, name="event"),

    # private endpoints
    path('login/', privateViews.adminLogin, name="login"),
    path('logout/', privateViews.adminLogout, name="logout"),
    path('addEvent/', privateViews.addEvent, name="addEvent"),
    path('deleteEvent/<int:pk>', privateViews.deleteEvent, name="deleteEvent"),
]
