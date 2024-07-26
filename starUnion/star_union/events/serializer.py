from rest_framework import serializers
from main.models import anonymous_user
from events.models import special_events_data, special_events
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

    # make the filed nullable
    first_name = serializers.CharField(max_length=50, allow_null=True)
    last_name = serializers.CharField(max_length=50, allow_null=True)
    email = serializers.EmailField(allow_null=True)
    phone = serializers.CharField(max_length=20, allow_null=True)
    university = serializers.CharField(max_length=50, allow_null=True)
    collage = serializers.CharField(max_length=50, allow_null=True)
    level = serializers.IntegerField(allow_null=True)
    gender = serializers.CharField(max_length=6, allow_null=True)

    def save(self,  event_name, *args, **kwargs):
        event_data = special_events_data.objects.all().filter(
            event__name=event_name, user__email=self.validated_data['email']).first()
        if event_data is not None:
            return {
                'message': 'You are already registered in this event'
            }
        user = anonymous_user.objects.create(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            phone=self.validated_data['phone'],
            email=self.validated_data['email'],
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
        return {
            'message': 'Done'
        }
