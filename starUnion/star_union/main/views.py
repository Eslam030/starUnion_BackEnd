from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from star_union.serializers import userSerializer
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.middleware import csrf
import jwt


# login view
def createUser(jsonData):
    # making user from from respose
    pass


class login (APIView):
    def post(self, request):
        ser = userSerializer(data=request.data)
        if ser.is_valid():
            response = JsonResponse({'message': 'Done'}, safe=False)
            response.set_cookie(
                'jwt', ser.validated_data.get("token"), samesite='None', secure=True
            )
            response["Access-Control-Allow-Headers"] = "true"

            # res = Response('{ "message" : "logged in successfully" }')
            # res['Access-Control-Allow-Credentials'] = True
            # res['Access-Control-Allow-Origin'] = True
            # # response = JsonResponse(
            # #     , safe=False)
            # # response.cookies['test'] = 'tests'
            # res.set_cookie(
            #     'jwt-token', ser.validated_data.get('token'))
            return response
        else:
            return JsonResponse('{message : "Fuck you mother fucker"}', safe=False)


class test (APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.COOKIES['jwt'])
        try:
            payload = jwt.decode(
                request.COOKIES['jwt'], settings.SECRET_KEY, algorithms=['HS256'])
            print(payload['user_id'])
            return HttpResponse("Done")
        except Exception:
            print(Exception)

            return HttpResponse("Expired")


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
