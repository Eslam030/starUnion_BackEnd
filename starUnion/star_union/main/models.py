from django.utils.safestring import mark_safe
from django.db import models
from django.contrib.auth.models import User


class user_profile_images (models.Model):
    photo = models.ImageField(upload_to='main/user_profile_images')

    def __str__(self) -> str:
        return str(self.photo).split("/")[-1]


class user (models.Model):
    class gender (models.TextChoices):
        male = "M"
        female = "F"

        def get(self, value):
            if value == "male":
                return self.male
            else:
                return self.female
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
    form = models.JSONField()

    def save(self, *args, **kwargs):
        self.form = str(self.form)

        super(*args, **kwargs).save()

    def __str__(self) -> str:
        return str(self.id)


class crew (user):
    role = models.TextField(max_length=50)
    rate = models.FloatField()

    def __str__(self) -> str:
        return super().__str__()


class optData (models.Model):
    otp = models.CharField(max_length=6)
    email = models.EmailField(unique=True)
    initTime = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.email
