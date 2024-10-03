from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .codeGenerator import CodeGenerator
from . import Event, RegistrationCode
from rest_framework.permissions import AllowAny

class RegisterOnEventApi(APIView):
    """
    Handles event registration by generating a unique code for a
    specific event. returns A JSON response with the generated code
    or an error message if the event is not found.
    """
    permission_classes = [AllowAny]
    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"error": f"Event with ID {pk} does not exist."}, status=status.HTTP_404_NOT_FOUND)

        codeLength = 8
        code = CodeGenerator(codeLength).generate_code()

        # Ensures the generated code is unique for the event, as there is still a 0.0000001% chance that codes could collide.
        while RegistrationCode.objects.filter(event=event, code=code).exists():
            codeLength += 1
            code = CodeGenerator(codeLength).generate_code()

        registration_code = RegistrationCode.objects.create(event=event, code=code)
        return Response({"code": code}, status=status.HTTP_200_OK)






