from django.shortcuts import render
from main.views import DefaultAPIView, AuthenticationAPIView
from . import models
from main.models import user, Forms
from django.http import JsonResponse, HttpResponseForbidden
from django.core import serializers
import json
from django.contrib.auth.models import User
from django.views import View
from django.db.models.query import QuerySet

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
        self.refreshResponseDate()
        workshops = None
        register = {}
        taking = {}
        if (request.GET.get('username') != None):
            # handle this
            rawUser = User.objects.all().filter(username=request.GET.get('username')).first()
            starUser = models.user.objects.all().filter(
                user=rawUser).first()
            workshops_user_taking = models.taking.objects.all().filter(
                participant=starUser)
            workshops = set()
            for workshop in workshops_user_taking:
                workshops.add(workshop.workshop)
                taking[workshop.workshop.name] = 1
            workshops_user_register = models.workshopRegister.objects.all().filter(
                user=starUser)
            for workshop in workshops_user_register:
                workshops.add(workshop.workshop)
                register[workshop.workshop.name] = 1
        elif (request.GET.get('workshop') != None):
            workshops = models.workshops.objects.all().filter(
                name=request.GET['workshop'])
        else:
            workshops = models.workshops.objects.all()
        # convert workshops from set to queryset

        if isinstance(workshops, set):
            temp_workshops = workshops
            all_workshops = models.workshops.objects.all()
            workshops = models.workshops.objects.none()
            for workshop in temp_workshops:
                workshops |= all_workshops.filter(name=workshop.name)

        workshops = workshops.order_by('-start_date')
        basic_workshopt_data = serializers.serialize('json', workshops)
        json_workshop_data = json.loads(basic_workshopt_data)
        for i in range(len(json_workshop_data)):
            del json_workshop_data[i]['model']
        for data in json_workshop_data:
            if data['pk'] in register:
                data['status'] = 'register'
            if data['pk'] in taking:
                data['status'] = 'taking'
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
        self.refreshResponseDate()
        return HttpResponseForbidden('Not Valid Right Now Coming Soon')


class registerForWorkshop (AuthenticationAPIView):
    def post(self, request):
        self.refreshResponseDate()
        operation = request.POST.get('operation')
        if operation == 'register':
            workshop = models.workshops.objects.all().filter(
                name=request.POST.get('workshop')).first()
            form = request.POST.get('form')
            form = Forms.objects.create(form=form)
            form.name = f"Form from {self.user.username} to register in {workshop.name}"

            userData = user.objects.all().filter(
                user=self.user).first()  # get the user from the token
            if workshop == None or form == None or userData == None:
                self.responseData['message'] = 'Invalid Data'
            else:
                try:
                    record = models.workshopRegister()
                    record.user = userData
                    record.workshop = workshop
                    record.form = form
                    record.save()
                    self.responseData['message'] = 'Done'
                except:
                    self.responseData['message'] = 'You Registered Before'
        elif operation == 'unregister':
            workshop = models.workshops.objects.all().filter(
                name=request.POST.get('workshop')).first()
            userData = user.objects.all().filter(
                user=self.user).first()
            registeredWorkshop = models.workshopRegister.objects.all().filter(
                user=userData, workshop=workshop).first()
            if registeredWorkshop == None:
                self.responseData['message'] = 'You are not registered in this workshop'
            else:
                registeredWorkshop.form.delete()
                registeredWorkshop.delete()
                takingWorkshop = models.taking.objects.all().filter(
                    participant=userData, workshop=workshop).first()
                if takingWorkshop != None:
                    takingWorkshop.delete()
                self.responseData['message'] = 'Done'
        return JsonResponse(self.responseData, safe=False)

    def get(self, request):
        # here will return a form the user can fill to register in the workshop
        self.refreshResponseDate()
        form = models.workshops.objects.all().filter(
            name=request.GET['name']).first().form
        self.responseData['messae'] = 'Done'
        self.responseData['form'] = form
        return JsonResponse(self.responseData, safe=False)


class top5(DefaultAPIView):
    def get(self, request):
        # here will return the top 5 students in specific workshop
        self.refreshResponseDate()
        student_taking = models.taking.objects.all().filter(
            workshop=request.GET['workshop']).order_by('-points')[:5]
        students = []
        for taking in student_taking:
            student = {}
            student['name'] = f"{taking.participant.user.first_name} {taking.participant.user.last_name}"
            student['points'] = taking.points
            student['photo'] = taking.participant.photo.photo.name
            students.append(student)
        self.responseData['data'] = students
        self.responseData['message'] = 'Done'
        return JsonResponse(self.responseData, safe=False)


class acceptWorkshop (View):
    # this made by the admin
    # should be a member or higher to accept user in workshop
    reponseData = {}

    def refreshResponseData(self):
        self.responseData = {}

    def isAccepted(self, user, workshop):
        if (models.taking.objects.all().filter(participant=user, workshop=workshop).first() != None):
            return True
        else:
            return False

    def get(self, request):
        # here will return the status of the user in the workshop
        self.refreshResponseData()
        if request.user != None and request.user.is_authenticated and request.user.is_staff:
            workshop = request.GET.get('workshop')
            username = request.GET.get('user')
            workshop = models.workshops.objects.all().filter(name=workshop).first()
            basicUser = User.objects.all().filter(username=username).first()
            starUser = user.objects.all().filter(user=basicUser).first()
            if workshop == None or starUser == None:
                self.responseData['message'] = 'Invalid Data'
            else:
                if self.isAccepted(starUser, workshop):
                    self.responseData['message'] = 'Accepted'
                else:
                    self.responseData['message'] = 'Not Accepted'
        else:
            return HttpResponseForbidden('Not Valid Right Now Coming Soon')
        return JsonResponse(self.responseData, safe=False)

    def post(self, request):
        # here will make the logic or accepting user in workshop
        self.refreshResponseData()
        if request.user != None and request.user.is_authenticated and request.user.is_staff:
            self.refreshResponseData()
            workshop = request.POST.get('workshop')
            username = request.POST.get('user')
            workshop = models.workshops.objects.all().filter(name=workshop).first()
            basicUser = User.objects.all().filter(username=username).first()
            starUser = user.objects.all().filter(user=basicUser).first()
            if workshop == None or starUser == None:
                self.responseData['message'] = 'Invalid Data'
            else:
                try:
                    record = models.taking()
                    record.participant = starUser
                    record.workshop = workshop
                    record.save()
                    self.responseData['message'] = 'Done'
                except:
                    self.responseData['message'] = 'You Accepted Before'
        else:
            return HttpResponseForbidden('Not Valid Right Now Coming Soon')
        return JsonResponse(self.responseData, safe=False)


class instructor (DefaultAPIView):
    def get(self, request):
        # here will return all instructors
        # if an id is given will return all instructors for a specific workshop
        self.refreshResponseDate()
        instructors = []
        instructing = None
        if (request.GET.get('workshop') != None):
            instructing = models.instructing.objects.all().filter(
                workshop=request.GET['workshop'])
        else:
            instructing = models.instructing.objects.all()
        for instructor_workshop in instructing:
            instructor = {}
            instructor['name'] = f"{instructor_workshop.instructor.member.user.first_name} {instructor_workshop.instructor.member.user.last_name}"
            instructor['username'] = instructor_workshop.instructor.member.user.username
            instructor['phtot'] = instructor_workshop.instructor.member.photo.photo.name
            if request.GET.get('worshop') == None:
                instructor['workshop'] = instructor_workshop.workshop.name
            instructors.append(instructor)
        self.responseData['data'] = instructors
        self.responseData['message'] = 'Done'
        return JsonResponse(self.responseData, safe=False)
        pass

    def post(self, request):
        # here will add an instructor
        self.refreshResponseDate()
        pass


class participant (DefaultAPIView):
    def get(self, request):
        # here will return all participants
        pass

    def post(self, request):
        # here will add a participant
        pass
