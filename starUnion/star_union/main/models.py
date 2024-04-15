from django.utils.safestring import mark_safe
from django.db import models
from django.contrib.auth.models import User


class user (models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=13)
    photo = models.ImageField(upload_to="users\\photos")
    university = models.CharField(max_length=50)
    collage = models.CharField(max_length=50)
    level = models.IntegerField()

    def __str__(self) -> str:
        return self.user.username


class BlackListed (models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)


class Forms (models.Model):
    form = models.JSONField()

    def save(self, *args, **kwargs):
        self.form = str(self.form)

        super(*args, **kwargs).save()

    def __str__(self) -> str:
        return self.form


class crew (user):
    role = models.TextField(max_length=50)
    rate = models.FloatField()


class optData (models.Model):
    otp = models.CharField(max_length=6)
    email = models.EmailField(unique=True)
    initTime = models.DateTimeField(auto_now_add=True)
