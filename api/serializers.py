# # eventmanager/serializers.py
#
from rest_framework import serializers  # Import your Event model
from . import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'  # This will include all fields of the Event model
