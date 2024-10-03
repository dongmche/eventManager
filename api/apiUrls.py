# api/apiUrls.py

from .getEventsServiceApi import GetEventsServiceApi
from .registerOnEventApi import RegisterOnEventApi
from .cancelEventApi import CancelEventApi
from .deleteEventApi import DeleteEvent
from .singleEventServiceApi import GetSingleEventApi
from .addEventServiceApi import AddEventService



from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # private api
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('addEvent/',  AddEventService.as_view(),name='events'),
    path('deleteEvent/<int:pk>/', (DeleteEvent.as_view()), name='deleteEvent'),

    # public Api
    path('events/', (GetEventsServiceApi.as_view()), name='events'),
    path('event/<int:pk>/', GetSingleEventApi.as_view(), name='getSingleEvent'),
    path('registerEvent/<int:pk>/', RegisterOnEventApi.as_view(), name='event-registration'),
    path('cancelRegistration/<int:pk>/<int:code>/', CancelEventApi.as_view(), name='cancel-registration'),
]
