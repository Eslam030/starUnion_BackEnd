from rest_framework import serializers
from django.contrib.auth.models import User
from events import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class userLoginSerializer (serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        # search for user to log him in
        user = authenticate(
            username=attrs['username'], password=attrs['password'])
        if user is not None:
            user = User.objects.all().filter(id=user.id).first()
            refresh = RefreshToken.for_user(user)
            return {
                'username': user.username,
                'email': user.email,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user
            }
        else:
            return {}


class userUpdataDeleteSerializer (serializers.Serializer):

    def create():
        pass

    def update():
        pass

# this will handle the data of the events and return all event data


class eventSerializer (serializers.Serializer):
    # will handle all things about the events
    # images names any related data
    def create():
        pass

    def update():
        pass


class workShopSerializer (serializers.Serializer):
    # will handle all things about the work shops
    # images names any related data

    def create():
        pass

    def update():
        pass
