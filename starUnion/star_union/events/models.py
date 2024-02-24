from django.db import models
from main.models import user, Forms


class photos (models.Model):
    photo = models.ImageField(upload_to="events\\Photos")


class events (models.Model):
    # Define the main events status that will be used
    class eventStatus (models.TextChoices):
        PAST = "PA"
        CurrentWorking = 'CW'
        Comming = 'CM'
    name = models.TextField(max_length=50)
    date = models.DateField()
    duration = models.IntegerField()
    status = models.CharField(max_length=2, choices=eventStatus.choices)
    location = models.TextField(max_length=50)
    logo = models.ImageField(upload_to="events\\Logos")
    event_photos = models.ManyToManyField(photos)


class sponsors (models.Model):
    name = models.TextField(max_length=50)
    mail = models.EmailField()
    logoPng = models.ImageField(upload_to="sponsors\\logos")
    deposit = models.FloatField()


class partnerships (models.Model):
    name = models.TextField(max_length=50)
    mail = models.EmailField()
    logoPng = models.ImageField(upload_to="partnerships\\logos")
    start_date = models.DateField()
    end_date = models.DateField()
    deposit = models.FloatField()


class attending (models.Model):
    event = models.ForeignKey(
        events,
        on_delete=models.CASCADE,
        related_name='event_attending'
    )
    attendee = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name='attendee'
    )


class sponsoring (models.Model):
    event = models.ForeignKey(
        events,
        on_delete=models.CASCADE,
        related_name='event_sponsoring'
    )
    sponsor = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name='sponsor'
    )
