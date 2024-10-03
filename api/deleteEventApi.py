from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from .serializers import EventSerializer
from . import Event
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class DeleteEvent(APIView):
    """
    private API service for deleting an event by its primary key (ID).
    """
    def delete(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response({"error": f"Event with id {pk} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        event.delete()
        return Response({"message": "Event deleted successfully!"}, status=status.HTTP_200_OK)


