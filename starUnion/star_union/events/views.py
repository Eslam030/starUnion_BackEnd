from main.views import DefaultAPIView, AuthenticationAPIView
from main.models import user  # will be needed in the comming deliveries
from . import models
from django.core import serializers
from django.http import JsonResponse
import json
from django.http import HttpResponseForbidden, HttpResponse


class events (DefaultAPIView):
    # No need for AuthenticationAPIView
    # Because there is no need for authentication
    # to get the events
    def get(self, request):  # for getting data about events
        # if an id is given will return all events for a specific user id
        # we can make it using the token !!
        # no because we want to make it public
        # and AuthenticationAPIView will need a token to operate
        events = None
        if (request.GET.get('id') != None):
            events = models.events.objects.all().filter(id=request.GET['id'])
        else:
            events = models.events.objects.all()
        basicEventData = serializers.serialize('json', events)
        jsonEventData = json.loads(basicEventData)
        for i in range(len(jsonEventData)):
            del jsonEventData[i]['model']
        self.responseData['data'] = jsonEventData
        self.responseData['message'] = 'Done'
        return JsonResponse(self.responseData, safe=False)

    def perform_authentication(self, request):
        # delete this function
        # to apply the custom funtion of AuthenticationAPIView
        return None

    def post(self, request):  # for create an event
        # and must have a token (done)
        # and must be a member or higher
        # will create event based on form using event serializer (next delivery!!!!!)
        # in this delivery creation will be from admin panel
        # then will be automated using a form

        # this block for only making the authentication
        # AuthenticationAPIView.perform_authentication(self, request)
        # self.responseData['message'] = 'done'
        # if self.updatedTokenAccess != None:
        #     self.responseData['access'] = self.updatedTokenAccess
        #     self.responseData['modified'] = True
        # return JsonResponse(self.responseData, safe=False)

        return HttpResponseForbidden('Not Valid Right Now Coming Soon')


class registerForEvent (AuthenticationAPIView):
    def post(self, request):
        # here will make the logic or registering user with event
        # using the event id and user id
        envet = request.POST.get('event')
        event = models.events.objects.all().filter(name=envet).first()
        if event != None:
            if event.status != models.events.eventStatus.PAST:
                record = models.attending()
                record.user = user.objects.all().filter(user=self.user).first()
                record.event = event
                record.save()
                self.responseData['message'] = 'Done'
            else:
                self.responseData['message'] = 'Event is already passed'
        else:
            self.responseData['message'] = 'Not valid event id'
        return JsonResponse(self.responseData, safe=False)


class sponsorsEvents (AuthenticationAPIView):
    def post(self, requst):
        # will make a relation between event and sponsor
        # and must have a token
        # and must be a member or higher
        # this will be done in the next delivery
        # we can make it manully from the admin panel (for now only)
        # in the next delivery will be more automated
        return HttpResponseForbidden('Not Valid Right Now Coming Soon')


class partnerSponsoringEvents (AuthenticationAPIView):
    def post(self, requst):
        # will make a relation between event and partener
        # and must have a token
        # and must be a member or higher
        # this will be done in the next delivery
        # we can make it manully from the admin panel (for now only)
        # in the next delivery will be more automated
        return HttpResponseForbidden('Not Valid Right Now Coming Soon')


class sponsors (DefaultAPIView):
    def get(self, request):
        # for getting data about sponsors
        # will return all data about the sponsors
        # if an id is given will return all sponsorsfor a specific event
        sponsors = None
        if (request.GET.get('id') != None):
            sponsors = models.sponsors.objects.all().filter(
                id=request.GET['id'])
        else:
            sponsors = models.sponsors.objects.all()
        basicSponsorData = serializers.serialize('json', sponsors)
        jsonSponsorData = json.loads(basicSponsorData)
        for i in range(len(jsonSponsorData)):
            del jsonSponsorData[i]['model']
        self.responseData['data'] = jsonSponsorData
        self.responseData['message'] = 'Done'
        return JsonResponse(self.responseData, safe=False)

    def perform_authentication(self, request):
        # delete this function
        # to apply the custom funtion of AuthenticationAPIView
        return None

    def post(self, request):  # for register a sponsor
        # and must be a member or higher
        # will create sponsor based on form using sponsor serializer (next delivery!!!!!)
        # in this delivery creation will be from admin panel
        # then will be automated using a form

        # this block for only making the authentication and authorization
        # AuthenticationAPIView.perform_authentication(self, request)
        # self.responseData['message'] = 'done'
        # if self.updatedTokenAccess != None:
        #     self.responseData['access'] = self.updatedTokenAccess
        #     self.responseData['modified'] = True
        # return JsonResponse(self.responseData, safe=False)
        return HttpResponseForbidden('Not Valid Right Now Coming Soon')


class partners (DefaultAPIView):
    def get(self, request):  # for getting data about parteners
        # will return all data about the parteners
        # if an id is given will return all parteners for a specific event
        parteners = None
        if (request.GET.get('id') != None):
            parteners = models.partnrships.objects.all().filter(
                id=request.GET['id'])
        else:
            parteners = models.partnrships.objects.all()
        basicPartenerData = serializers.serialize('json', parteners)
        jsonPartenerData = json.loads(basicPartenerData)
        for i in range(len(jsonPartenerData)):
            del jsonPartenerData[i]['model']
        self.responseData['data'] = jsonPartenerData
        self.responseData['message'] = 'Done'
        return JsonResponse(self.responseData, safe=False)

    def perform_authentication(self, request):
        # delete this function
        # to apply the custom funtion of AuthenticationAPIView
        return None

    def post(self, request):  # for register a partener
        # and must be a member or higher
        # will create partener based on form using partener serializer (next delivery!!!!!)
        # in this delivery creation will be from admin panel
        # then will be automated using a form

        # this block for only making the authentication and authorization
        # AuthenticationAPIView.perform_authentication(self, request)
        # self.responseData['message'] = 'done'
        # if self.updatedTokenAccess != None:
        #     self.responseData['access'] = self.updatedTokenAccess
        #     self.responseData['modified'] = True
        # return JsonResponse(self.responseData, safe=False)
        return HttpResponseForbidden('Not Valid Right Now Coming Soon')
