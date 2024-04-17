from rest_framework import serializers
from django.contrib.auth import authenticate
from main.models import user_profile_images, user
from django.contrib.auth.models import User
from events import models
from rest_framework_simplejwt.tokens import RefreshToken


class gender_creator():
    def __init__(self, value):
        self.value = value

    def get(self):
        if self.value.lower() == 'male':
            return user.gender.male
        elif self.value.lower() == 'female':
            return user.gender.female


class userSerializer (serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    gender = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    phone = serializers.CharField()
    university = serializers.CharField()
    collage = serializers.CharField()
    level = serializers.IntegerField()
    photo = serializers.CharField()

    def create(self, validated_data):
        if User.objects.all().filter(username=validated_data['username']).first() is not None:
            return {
                'message': 'Username Exists'
            }
        if User.objects.all().filter(email=validated_data['email']).first() is not None:
            return {
                'message': 'Email Exists'
            }
        username = validated_data['username']
        djangoUser = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password']
        )
        djangoUser.save()
        user = models.user(
            user=djangoUser,
            phone=validated_data['phone'],
            university=validated_data['university'],
            collage=validated_data['collage'],
            level=validated_data['level'],
        )
        user.photo = user_profile_images.objects.all().filter(
            id=validated_data['photo']).first()
        user.gen = gender_creator(validated_data['gender']).get()
        user.save()
        return {
            'message': 'Done',
            'user': user
        }

    def update(self, instance, validated_data):
        if User.objects.all().filter(username=validated_data['username']).first() is not None:
            return {
                'message': 'Username Exists'
            }
        if User.objects.all().filter(email=validated_data['email']).first() is not None:
            return {
                'message': 'Email Exists'
            }
        instance.user.username = validated_data.get(
            'username', instance.user.username)
        instance.user.email = validated_data.get('email', instance.user.email)
        instance.user.save()
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.university = validated_data.get(
            'university', instance.university)
        instance.collage = validated_data.get('collage', instance.collage)
        instance.level = validated_data.get('level', instance.level)
        instance.save()
        return instance


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
                'username': user,
                'email': user.email,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user
            }
        else:
            return {}
