from .serializers import EventSerializer
from . import Event
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime

class AddEventService(APIView):
    """
    private API service for adding a new event.

    **Description:**
    This service allows authenticated administrators to create new events by submitting
    the required fields: title, start date, end date, and a thumbnail URL. The API validates
    the request and, if all data is valid, creates the event in the database.

    **Response:**
    - **201 Created**: Event created successfully.
    - **400 Bad Request**: If required fields are missing or invalid (e.g., invalid date format).
    - **500 Internal Server Error**: If an unexpected error occurs during processing.

    **Notes:**
    - Ensure that the request has valid authentication and provides a valid JWT token in the `Authorization` header.
    - The `start_date` and `end_date` should follow the ISO 8601 format (e.g., "2024-10-03T10:00:00Z").
    - The event thumbnail is optional and should be a valid URL if provided.
    """

    def post(self, request):
        try:
            # Extracting data from the request
            title = request.data.get('title')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            thumbnail = request.data.get('thumbnail')  # Get the thumbnail URL from the request

            # Validate the required fields
            if not title or not start_date or not end_date:
                return Response({"error": "All fields (title, start_date, end_date) are required."},
                                status=status.HTTP_400_BAD_REQUEST)


            # Parse the dates
            try:
                start_date = parse_datetime(start_date)
                end_date = parse_datetime(end_date)
            except ValueError:
                return Response({"error": "Invalid date format."}, status=status.HTTP_400_BAD_REQUEST)

            if start_date > end_date:
                return Response({"error": "Incorrect dates."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the event with the thumbnail URL
            event = Event.objects.create(title=title, start_date=start_date, end_date=end_date, thumbnail=thumbnail)
            event.save()

            return Response({"message": "Event created successfully!"}, status=status.HTTP_201_CREATED)

        # Catch any other unexpected exceptions
        except Exception as e:
            return Response({"error": "An internal error occurred."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


