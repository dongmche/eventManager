from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=50)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    thumbnail = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.title


class RegistrationCode(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registration_codes')
    code = models.CharField(max_length=20, unique=True)  # You can adjust the length
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)  # Boolean field with a default value of False
    email = models.EmailField(null=True, blank=True)  # Email field to store email addresses
    verification_code = models.CharField(max_length=20, null=True, blank=True)


class Meta:
    unique_together = ('event', 'code')  # Ensures uniqueness of the code for each event

    def __str__(self):
        return f'{self.code} for {self.event.title}'
