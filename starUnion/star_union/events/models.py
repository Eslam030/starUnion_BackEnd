from django.db import models
from main.models import user, anonymous_user
from django.conf import settings
from django import forms
from django.conf import settings


# how photos will be stored ??
# at this phase as we use un customized amin dashboard
# we will at first store photo in temp_photos folder
# then after save will be replaced to the right folder
class photos (models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    photo = models.ImageField(
        upload_to=settings.BASE_DIR / "events" / "temp_photos" , max_length=500)

    def __str__(self) -> str:
        return str(self.photo.path).split("\\")[-1]


class events (models.Model):
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
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
    logo = models.ImageField(blank=True, null=True , max_length=500)
    event_photos = models.ManyToManyField(photos,  blank=True)
    description = models.TextField(blank=True, default='')

    def __str__(self) -> str:
        return self.name


class company (models.Model):
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
    name = models.CharField(max_length=50, primary_key=True)
    mail = models.EmailField()
    logo = models.ImageField(blank=True, default='' ,max_length=500)

    def __str__(self) -> str:
        return self.name


class special_events (events):
    class Meta:
        verbose_name = 'Special Event'
        verbose_name_plural = 'Special Events'
    company = models.ForeignKey(company, on_delete=models.CASCADE)
    form_photo = models.ImageField(blank=True , max_length=500 , default='')

    def __str__(self) -> str:
        return self.name + " __ " + self.company.name


class special_events_data (models.Model):
    class Meta:
        verbose_name = 'Special Event Data'
        verbose_name_plural = 'Special Events Data'
    event = models.ForeignKey(special_events, on_delete=models.CASCADE)
    user = models.OneToOneField(anonymous_user, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.event.name + " __ " + self.user.first_name + " " + self.user.last_name


class sponsors (models.Model):
    class Meta:
        verbose_name = 'Sponsor'
        verbose_name_plural = 'Sponsors'
    name = models.CharField(max_length=50, primary_key=True)
    mail = models.EmailField()
    logo = models.ImageField(blank=True , max_length=500)
    deposit = models.FloatField()

    def __str__(self) -> str:
        return self.name


class partnrships (models.Model):
    class Meta:
        verbose_name = 'Partnership'
        verbose_name_plural = 'Partnerships'
    name = models.CharField(max_length=50, primary_key=True)
    mail = models.EmailField()
    logo = models.ImageField(blank=True , max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    deposit = models.FloatField()

    def __str__(self) -> str:
        return self.name


class partnerForm (forms.ModelForm):
    class Meta:
        model = partnrships
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['start_date'] > cleaned_data['end_date']:
            raise forms.ValidationError(
                "The start date must be before the end date")
        return cleaned_data


class attending (models.Model):
    event = models.ForeignKey(events, on_delete=models.CASCADE)
    user = models.ForeignKey(user, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Event : " + self.event.name + " __ attendee : " + self.user.user.username

    class Meta:
        verbose_name = 'Attending'
        verbose_name_plural = 'Attendings'
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
        verbose_name = 'Sponsoring'
        verbose_name_plural = 'Sponsorings'
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'sponsor'], name='composite_event_sponsor_pk')
        ]


class partnerSponsoring (models.Model):
    event = models.ForeignKey(events, on_delete=models.CASCADE)
    partner = models.ForeignKey(partnrships, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "Event : " + self.event.name + " __ Partner : " + self.partner.name

    class Meta:
        verbose_name = 'Partner Sponsoring'
        verbose_name_plural = 'Partner Sponsorings'
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'partner'], name='composite_event_sponsor_partener_pk')
        ]
