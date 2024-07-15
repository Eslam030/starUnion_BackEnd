from rest_framework import serializers
from main.models import anonymous_user
from events.models import special_events_data , special_events
from main.serializer import gender_creator

# will be implemented in the upcoming versions


class eventSerializer (serializers.Serializer):
    # will handle all things about the events
    # images names any related data
    def create():
        pass

    def update():
        pass


class specialEventRegisterSerializer (serializers.Serializer):
    # will handle all things about the special events
    # images names any related data
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    university = serializers.CharField(max_length=50)
    collage = serializers.CharField(max_length=50)
    level = serializers.IntegerField()
    gender = serializers.CharField(max_length=5)

    def save (self ,  event_name , *args , **kwargs ):
        user = anonymous_user.objects.create(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            phone=self.validated_data['phone'],
            university=self.validated_data['university'],
            collage=self.validated_data['collage'],
            level=self.validated_data['level'],
            gen=gender_creator(self.validated_data['gender']).get()
        )
        event = special_events.objects.get(name=event_name)

        special_events_data.objects.create(
            event=event,
            user=user
        )
        