from django.db import models
from main.models import user, crew, Forms


class photos (models.Model):
    image = models.ImageField(upload_to="workshops\\photos")


class workshops (models.Model):
    # Define the main events status that will be used
    class workshopStatus (models.TextChoices):
        PAST = "PA"
        CurrentWorking = 'CW'
        Comming = 'CM'
    name = models.CharField(max_length=50, primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.FloatField()
    duration = models.DurationField()
    availability = models.BooleanField()
    status = models.CharField(max_length=2, choices=workshopStatus.choices)
    # location is saved as the embbaded google maps link
    location = models.CharField(max_length=512)
    logo = models.ImageField(blank=True)
    workshop_photos = models.ManyToManyField(photos,  blank=True)
    content = models.JSONField()
    form = models.JSONField()

    def __str__(self) -> str:
        return self.name

    # override the save method to save the logo in the right folder
    def save(self, *args, **kwargs):
        if "/" not in str(self.logo):
            self.logo.name = "workshops/EveryWorkshopData/" + \
                self.name + "/logos/" + self.logo.name
        super(*args, **kwargs).save()


class instructing (models.Model):
    instructor = models.ForeignKey(
        crew,
        on_delete=models.CASCADE,
    )
    workshop = models.ForeignKey(
        workshops,
        on_delete=models.CASCADE,
    )


class taking (models.Model):
    participant = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
    )
    workshop = models.ForeignKey(
        workshops,
        on_delete=models.CASCADE,
    )


class W_Register (models.Model):
    form = models.ForeignKey(
        Forms,
        on_delete=models.CASCADE,
    )
    workshop = models.ForeignKey(
        workshops,
        on_delete=models.CASCADE,
    )
