from django.utils.safestring import mark_safe
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class user_profile_images (models.Model):
    photo = models.ImageField(max_length=500)

    def __str__(self) -> str:
        wanted_photo = str(self.photo).replace("\\" , "/")
        return wanted_photo.split("/")[-1]
    


class user (models.Model):
    class gender (models.TextChoices):
        male = "M"
        female = "F"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=13)
    photo = models.ForeignKey(user_profile_images, on_delete=models.CASCADE)
    university = models.CharField(max_length=50)
    collage = models.CharField(max_length=50)
    level = models.IntegerField()
    gen = models.CharField(choices=gender.choices, max_length=1)

    def __str__(self) -> str:
        return self.user.username


class anonymous_user (models.Model):
    class gender (models.TextChoices):
        male = "M"
        female = "F"

    first_name = models.CharField(max_length=50 , null=True , default='') 
    last_name = models.CharField(max_length=50 , null=True , default='')
    email = models.EmailField(default="")
    phone = models.CharField(max_length=20 , null=True , default='')
    university = models.CharField(max_length=50 , null=True , default='')
    collage = models.CharField(max_length=50 , null=True , default='')
    level = models.IntegerField()
    gen = models.CharField(choices=gender.choices, max_length=1 , null=True , default='')

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class crew (models.Model):
    member = models.OneToOneField(
        user, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=50)
    rate = models.FloatField()

    def __str__(self) -> str:
        return self.member.user.username


class user_refresh_token (models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    token = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.user.username


class BlackListed (models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self) -> str:
        return self.user.username


class Forms (models.Model):
    name = models.CharField(max_length=50, default="form")
    form = models.JSONField()

    def __str__(self) -> str:
        return str(self.name)


class optData (models.Model):
    otp = models.CharField(max_length=6)
    email = models.EmailField(unique=True)
    initTime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.email
