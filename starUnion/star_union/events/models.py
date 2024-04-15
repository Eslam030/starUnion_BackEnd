from django.db import models
from main.models import user
from django.contrib.auth.models import User


# how photos will be stored ??
# at this phase as we use un customized amin dashboard
# we will at first store photo in temp_photos folder
# then after save will be replaced to the right folder
class photos (models.Model):
    photo = models.ImageField(upload_to="events/temp_photos")

    def __str__(self) -> str:
        return str(self.photo.path).split("\\")[-1]


class events (models.Model):
    # Define the main events status that will be used
    class eventStatus (models.TextChoices):
        PAST = "PA"
        CurrentWorking = 'CW'
        Comming = 'CM'
    name = models.CharField(max_length=50, primary_key=True)
    date = models.DateField()
    duration = models.DurationField()
    status = models.CharField(max_length=2, choices=eventStatus.choices)
    # location is saved as the embbaded google maps link
    location = models.CharField(max_length=512)
    logo = models.ImageField(blank=True)
    event_photos = models.ManyToManyField(photos,  blank=True)

    def __str__(self) -> str:
        return self.name

    # override the save method to save the logo in the right folder
    def save(self, *args, **kwargs):
        if "/" not in str(self.logo):
            self.logo.name = "events/EveryEventData/" + \
                self.name + "/logos/" + self.logo.name
        super(*args, **kwargs).save()


class sponsors (models.Model):
    name = models.TextField(max_length=50)
    mail = models.EmailField()
    logo = models.ImageField(blank=True)
    deposit = models.FloatField()

    # override the save method to save the logo in the right folder
    def save(self, *args, **kwargs):
        if "/" not in str(self.logo):
            self.logo.name = "events/EverySponsorData/" + \
                self.name + "/logos/" + self.logo.name
        super(*args, **kwargs).save()

    def __str__(self) -> str:
        return self.name


class partnrships (models.Model):
    name = models.TextField(max_length=50)
    mail = models.EmailField()
    logo = models.ImageField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    deposit = models.FloatField()

    # override the save method to save the logo in the right folder
    def save(self, *args, **kwargs):
        if "/" not in str(self.logo):
            self.logo.name = "events/EveryPartenerData/" + \
                self.name + "/logos/" + self.logo.name
        super(*args, **kwargs).save()

    def __str__(self) -> str:
        return self.name


class attending (models.Model):
    event = models.ForeignKey(events, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Event : " + self.event.name + " __ attendee : " + self.user.user.username

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'user'], name='composite_event_attendee_pk')
        ]


class sponsoring (models.Model):
    event = models.ForeignKey(events, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(sponsors, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Event : " + self.event.name + " __ Sponsor : " + self.sponsor.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'sponsor'], name='composite_event_sponsor_pk')
        ]


class partner_sponsoring (models.Model):
    event = models.ForeignKey(events, on_delete=models.CASCADE)
    partner = models.ForeignKey(partnrships, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Event : " + self.event.name + " __ Partner : " + self.partner.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'partner'], name='composite_event_sponsor_partener_pk')
        ]
