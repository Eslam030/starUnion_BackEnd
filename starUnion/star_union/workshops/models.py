from django.db import models
from main.models import user, crew, Forms


class photos (models.Model):
    image = models.ImageField(upload_to="workshops\\photos")


class workshops (models.Model):
    # Define the main workshops status that will be used
    class workshopStatus (models.TextChoices):
        PAST = "PA"
        CurrentWorking = 'CW'
        Comming = 'CM'

    name = models.TextField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.FloatField()
    status = models.CharField(max_length=2, choices=workshopStatus.choices)
    availability = models.BooleanField()
    logo = models.ImageField(upload_to="workshops\\logos")
    content = models.JSONField()
    workshop_photos = models.ManyToManyField(photos)


class instructing (models.Model):
    instructor = models.ForeignKey(
        crew,
        on_delete=models.CASCADE,
        related_name='workshop_instructor'
    )
    workshop = models.ForeignKey(
        workshops,
        on_delete=models.CASCADE,
        related_name='giving_workshop'
    )


class taking (models.Model):
    participant = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name='workshop_participant'
    )
    workshop = models.ForeignKey(
        workshops,
        on_delete=models.CASCADE,
        related_name='attending_workshop'
    )


class W_Register (models.Model):
    form = models.ForeignKey(
        Forms,
        on_delete=models.CASCADE,
        related_name='form_register'
    )
    workshop = models.ForeignKey(
        workshops,
        on_delete=models.CASCADE,
        related_name='workshop_register'
    )
