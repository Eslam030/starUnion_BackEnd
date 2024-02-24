from django.db import models
from django.contrib.auth.models import User


class user (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    photo = models.ImageField(upload_to="users\\photos")
    university = models.CharField(max_length=50)
    collage = models.CharField(max_length=50)
    level = models.IntegerField()


class Forms (models.Model):
    form = models.JSONField()


class crew (user):
    role = models.TextField(max_length=50)
    rate = models.FloatField()
