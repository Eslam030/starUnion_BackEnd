from rest_framework import serializers
from django.contrib.auth import authenticate
from main.models import user_profile_images, user
from django.contrib.auth.models import User
from events import models
from rest_framework_simplejwt.tokens import RefreshToken
from enum import Enum

import re


def is_valid_email(email):
    # Regular expression pattern for validating email addresses
    pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


class gender_creator():
    def __init__(self, value):
        self.value = value

    def get(self):
        if self.value.lower() == 'male':
            return user.gender.male
        elif self.value.lower() == 'female':
            return user.gender.female


class userCreationSerializer (serializers.Serializer):
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
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
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
            photo__contains=f'{validated_data['gender'].lower().capitalize()}.png').first()
        user.gen = gender_creator(validated_data['gender']).get()
        user.save()
        return {
            'message': 'Done',
            'user': user
        }


class userUpdateSerializer (serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.CharField()
    phone = serializers.CharField()
    university = serializers.CharField()
    collage = serializers.CharField()
    level = serializers.IntegerField()
    photo = serializers.CharField()

    def update(self, instance, validated_data):
        instance = user.objects.all().filter(user=instance).first()
        instance.user.first_name = validated_data.get(
            'first_name')
        instance.user.last_name = validated_data.get(
            'last_name')
        instance.user.save()
        instance.phone = validated_data.get('phone')
        instance.university = validated_data.get(
            'university')
        instance.collage = validated_data.get('collage')
        instance.level = validated_data.get('level')
        instance.photo = user_profile_images.objects.all().filter(
            photo__contains=validated_data['photo']).first()
        instance.save()
        return {
            'message': 'Done',
        }


class userLoginSerializer (serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        # search for user to log him in
        if is_valid_email(attrs['username_or_email']):
            user = User.objects.all().filter(
                email=attrs['username_or_email']).first()
            if user is not None:
                user = authenticate(
                    username=user.username, password=attrs['password'])
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
            else:
                return {}
        else:
            user = authenticate(
                username=attrs['username_or_email'], password=attrs['password'])
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
