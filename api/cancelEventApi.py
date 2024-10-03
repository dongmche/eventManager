from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import Event, RegistrationCode
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny

def canCancelEvent(event) -> bool:
    """
    Check if the event lasts no longer than two days and if it's not
    later than two days before the event's start date.
    Returns bool: True if the event can be canceled, False otherwise.
    """

    event_duration = event.end_date - event.start_date

    if event_duration > timedelta(days=2):
        return False

    from django.utils import timezone
    current_date = timezone.now()

    if event.start_date - current_date < timedelta(days=2):
        return False
    return True

class CancelEventApi(APIView):
    """
    Deletes the registration code for the event with the given ID.
    Returns A JSON response indicating success or failure.
    """
    permission_classes = [AllowAny]
    def delete(self, request, pk, code):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": f" Event id {pk} does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        if not canCancelEvent(event):
            return Response(
                {"error": "Event cannot be canceled. It either lasts more than two days "
                          "or it's too close to the start date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            registration_code = RegistrationCode.objects.get(event=pk, code=code)
            registration_code.delete()
            return Response({"message": f"Registration code {code} for event ID {pk} deleted successfully."},
                            status=status.HTTP_200_OK)
        except RegistrationCode.DoesNotExist:
            return Response({"error": f"Registration code {code} does not exist for this event."},
                            status=status.HTTP_404_NOT_FOUND)
