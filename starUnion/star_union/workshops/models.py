from django.db import models
from main.models import user, crew, Forms
from django import forms


class photos (models.Model):
    photo = models.ImageField(upload_to="workshops\\photos")

    def __str__(self):
        return self.photo.name.split("\\")[-1]


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
    content = models.JSONField(default="{}")
    form = models.JSONField(default="{}")

    def __str__(self) -> str:
        return self.name


class instructing (models.Model):
    instructor = models.ForeignKey(crew, on_delete=models.CASCADE)
    workshop = models.ForeignKey(workshops, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['instructor', 'workshop'], name='composite_workshop_instructor_pk')
        ]

    def __str__(self):
        return f"{self.instructor.firtname} {self.instructor.firtname} instructing {self.workshop.name}"


class workshopForm (forms.ModelForm):
    class Meta:
        model = workshops
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['start_date'] > cleaned_data['end_date']:
            raise forms.ValidationError(
                "The start date must be before the end date")
        return cleaned_data


class taking (models.Model):
    participant = models.ForeignKey(user, on_delete=models.CASCADE)
    workshop = models.ForeignKey(workshops, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['participant', 'workshop'], name='composite_workshop_participant_pk')
        ]

    def __str__(self):
        return f"{self.participant.firtname} {self.participant.firtname} taking {self.workshop.name}"


class workshopRegister (models.Model):
    form = models.ForeignKey(Forms, on_delete=models.CASCADE)
    workshop = models.ForeignKey(workshops, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['form', 'workshop'], name='composite_workshop_form_pk')
        ]

    def __str__(self):
        return f"{self.form.id} for {self.workshop.name}"
