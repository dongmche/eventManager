# api/getEventsServiceApi.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from .serializers import EventSerializer
from . import Event
from rest_framework.permissions import IsAuthenticated, AllowAny



class GetEventsServiceApi(APIView):
    """
    API endpoint to return a list of events (GET is public).
    """
    permission_classes = [AllowAny]
    def get(self, request):
        events = Event.objects.all()  # Query all events from the database
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





