from django.shortcuts import render
from main.views import DefaultAPIView, AuthenticationAPIView
from . import models
from django.http import JsonResponse, HttpResponseForbidden
from django.core import serializers
import json

# Create your views here.


class workshop (DefaultAPIView):
    # No need for AuthenticationAPIView
    # Because there is no need for authentication
    # to get the workshops
    def get(self, request):  # for getting data about workshop
        # if an id is given will return all workshops for a specific user id
        # we can make it using the token !!
        # no because we want to make it public
        # and AuthenticationAPIView will need a token to operate
        workshops = None
        if (request.GET.get('id') != None):
            workshops = models.workshops.objects.all().filter(
                id=request.GET['id'])
        else:
            workshops = models.workshops.objects.all()
        basic_workshopt_data = serializers.serialize('json', workshops)
        json_workshop_data = json.loads(basic_workshopt_data)
        for i in range(len(json_workshop_data)):
            del json_workshop_data[i]['model']
        self.responseData['data'] = json_workshop_data
        self.responseData['message'] = 'Done'
        return JsonResponse(self.responseData, safe=False)

    def perform_authentication(self, request):
        # delete this function
        # to apply the custom funtion of AuthenticationAPIView
        return None

    def post(self, request):  # for create an workshop
        # and must have a token (done)
        # and must be a member or higher
        # will create workshop based on form using workshop serializer (next delivery!!!!!)
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


class registerForWorkshop (AuthenticationAPIView):
    def post(self, request):
        # here will make the logic or registering user with workshop
        pass

    def get(self, request):
        # here will return a form the user can fill to register in the workshop
        pass


class acceptWorkshop (AuthenticationAPIView):
    # should be a member or higher to accept user in workshop
    def post(self, request):
        # here will make the logic or accepting user in workshop
        pass


class instructor (DefaultAPIView):
    def get(self, request):
        # here will return all instructors
        pass

    def post(self, request):
        # here will add an instructor
        pass


class participant (DefaultAPIView):
    def get(self, request):
        # here will return all participants
        pass

    def post(self, request):
        # here will add a participant
        pass
