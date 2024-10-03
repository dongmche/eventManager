from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from .serializers import EventSerializer
from . import Event
from rest_framework.permissions import IsAuthenticated, AllowAny


class GetSingleEventApi(APIView):
    """
    API endpoint to return an event based on pk (GET is public).
    """
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            event = Event.objects.get(id=pk)
        except Event.DoesNotExist:
            return Response({"error": f"Event with id {pk} does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventSerializer(event)

        return Response(serializer.data, status=status.HTTP_200_OK)