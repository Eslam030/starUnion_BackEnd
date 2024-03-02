from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class userSerializer (serializers.Serializer):
    username = serializers.CharField()
    id = serializers.IntegerField()
    password = serializers.CharField()

    def create(self):
        pass

    def update(self):
        pass

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
                'token': str(refresh.access_token),
            }
        else:
            return {
                'message': 'duck'
            }
