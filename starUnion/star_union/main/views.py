from django.shortcuts import render
from django.views import View

# login view


def createUser(jsonData):
    # making user from from respose
    pass


class login (View):
    def post(self, request):
        pass


class otp (View):
    def otpgen():
        pass

    def post(self, request):  # for sending otp
        pass

    def get(self, request):  # for checking otp
        pass


class upgrade (View):
    pass


class updateData (View):
    def put(self, request):
        pass


class changePass (View):
    def put(self, request):
        pass
