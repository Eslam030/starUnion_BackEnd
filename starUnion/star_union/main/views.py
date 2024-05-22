from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializer import userLoginSerializer, userCreationSerializer, userUpdateSerializer
from .models import *
from django.http import JsonResponse, HttpResponse
import json
from django.conf import settings
from jwt import PyJWS
import jwt
from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken
import time
import datetime
import pyotp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pytz
from main.mail_template import otpMailTemplate
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
# this custom APIView for classes that
# i want to handle the expiration of the token i a custom way
# not just raise Not authentication Exception when it is expired


class DefaultAPIView (APIView):
    responseData = {}

    # this function to refresh the response data in each request
    # it actully used in each request
    # you can see it in the top of each request function
    def refreshResponseDate(self):
        self.responseData = {}


class AuthenticationAPIView (DefaultAPIView):
    # handling the tokens with the priviladge endpoints
    user = None

    def perform_authentication(self, request):
        # This to assign an attribute indicates if the token is modified or not
        self.updatedTokenAccess = None
        try:
           # loads the token data using PyJWS (int JWT library files)
            token = request.headers['Authorization'][4:]
            tokenData = PyJWS._load(
                self, jwt=token)
            # the content is loaded in binary so converting it to string and json to access the data
            # in side the token data
            # !! you can print to view the data
            tokenJson = json.loads(str(tokenData[0])[2:-1])
            user_id = tokenJson['user_id']
            self.user = User.objects.all().filter(
                id=user_id).first()
            refresh_token = user_refresh_token.objects.all().filter(user=self.user).first()
            if refresh_token != None:
                token = PyJWS._load(self, jwt=refresh_token.token)
                refresh_token_data = json.loads(str(token[0])[2:-1])
                if refresh_token_data['exp'] < time.time():
                    BlackListed.objects.create(user=self.user)
            black = BlackListed.objects.all().filter(user=self.user).first()
            if black != None:
                raise exceptions.NotAuthenticated
            if tokenJson['exp'] < time.time():
                # check the expiry of the token
                # if it is expired and there is a user with a credentials
                # and the token is valid so just refresh the token
                # and send back the access key to client side
                # get the user id to check if the user is actually exist
                if self.user != None:
                    # if the user credentials are true
                    # just refresh user token again
                    refreshedToken = RefreshToken.for_user(self.user)
                    jwt.decode(str(refreshedToken.access_token).encode('utf-8'),
                               settings.SECRET_KEY, 'HS256')

                    if refresh_token != None:

                        refresh_token.token = refreshedToken
                        refresh_token.save()

                    else:
                        refresh_token.objects.create(
                            user=self.user, token=refreshedToken)
                    self.updatedTokenAccess = str(refreshedToken.access_token)
                    self.updateRefreshToken = str(refreshedToken)
                else:
                    raise exceptions.NotAuthenticated
            else:
                # check the secret key
                # if the secret key is not valid
                # of if the secret key is changed
                # unauthorize all logged in users
                jwt.decode(str(request.headers['Authorization'][4:]).encode('utf-8'),
                           settings.SECRET_KEY, 'HS256')
        except Exception as ex:
            raise exceptions.NotAuthenticated

# done


class login (DefaultAPIView):
    def post(self, request):
        self.refreshResponseDate()
        ser = userLoginSerializer(data=request.data)
        if ser.is_valid():
            if len(ser.validated_data) == 0:
                self.responseData['message'] = 'Not valid credentials'
            else:

                black = BlackListed.objects.all().filter(user=ser.validated_data.get('user'))
                if black != None:
                    black.delete()
                self.responseData['message'] = 'done'
                self.responseData['access'] = ser.validated_data.get('access')
                self.responseData['refrest'] = ser.validated_data.get(
                    'refresh')
                self.responseData['user'] = ser.validated_data.get(
                    'user').username
                refresh_token = user_refresh_token.objects.all().filter(
                    user=ser.validated_data.get('user')).first()
                if refresh_token != None:
                    refresh_token.token = ser.validated_data.get('refresh')
                    refresh_token.save()
                else:
                    user_refresh_token.objects.create(user=ser.validated_data.get(
                        'user'), token=ser.validated_data.get('refresh'))
        else:
            self.responseData['message'] = 'Not valid credentials'

        return JsonResponse(self.responseData, safe=False)


class logout(AuthenticationAPIView):
    def post(self, request):
        self.refreshResponseDate()
        self.responseData['message'] = 'done'
        record = BlackListed()
        record.user = self.user
        record.save()
        return JsonResponse(self.responseData, safe=False)


class register (DefaultAPIView):
    def post(self, request):
        self.refreshResponseDate()
        # get the data from the request
        ser = userCreationSerializer(data=request.data)
        if ser.is_valid():
            response = ser.create(ser.validated_data)
            self.responseData['message'] = response['message']
        else:
            self.responseData['message'] = 'Not valid data'
        return JsonResponse(self.responseData, safe=False)

    def get(self, request):
        self.refreshResponseDate()
        if request.GET['email'] != None and request.GET['username']:
            if User.objects.all().filter(username=request.GET['username']).first() != None:
                self.responseData['message'] = 'Username Exists'
            elif User.objects.all().filter(email=request.GET['email']).first() != None:
                self.responseData['message'] = 'Email Exists'
            else:
                self.responseData['message'] = 'Done'
        else:
            self.responseData['message'] = 'Not valid data'
        return JsonResponse(self.responseData, safe=False)
    # using user serlializer and form submited


class updateToken (AuthenticationAPIView):
    def post(self, request):
        self.refreshResponseDate()
        if self.updatedTokenAccess != None:
            self.responseData['access'] = self.updatedTokenAccess
            self.responseData['modified'] = True
        else:
            self.responseData['modified'] = False
        return JsonResponse(self.responseData, safe=False)


class otp (DefaultAPIView):
    otp_duration_in_minutes = 3

    def post(self, request):
        self.refreshResponseDate()
        # for sending otp
        # Generate a random base32 secret key
        secret = pyotp.random_base32()
        # Create a TOTP object using the secret key
        totp = pyotp.TOTP(secret)
        # Generate an OTP
        otp = totp.now()
        senderEmail = 'esla889900@gmail.com'
        receverEmail = request.POST['email']
        message = MIMEMultipart()
        message["From"] = senderEmail
        message["To"] = receverEmail
        message["Subject"] = "Star Union OTP For Registration"
        # will here attach the logo after we deploy the server

        body = otpMailTemplate(
            otp, "https://starunion.pythonanywhere.com/main/getImage/?path=star_union/assets/logo.png").getTemplate()
        message.attach(MIMEText(body, "html"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(senderEmail, "zzzg qfzc cszc fqhw")
            text = message.as_string()
            server.sendmail(senderEmail,
                            receverEmail, text)
        record = optData.objects.all().filter(email=receverEmail).first()
        if record != None:
            record.otp = otp
            record.save()
        else:
            newRecord = optData()
            newRecord.email = receverEmail
            newRecord.otp = otp
            newRecord.initTime = timezone.now()
            newRecord.save()
        return JsonResponse({'message': 'Done get OTP'})
        # getting the email from the request

    def checkOtp(self, email, otp):
        self.refreshResponseDate()
        record = optData.objects.all().filter(email=email).first()
        if record != None:
            currentDate = datetime.datetime.now(pytz.timezone('Africa/Cairo'))
            delta = currentDate - record.initTime
            datla = delta.total_seconds() / 60
            exipryMinutes = datetime.timedelta(
                minutes=self.otp_duration_in_minutes)
            if delta > exipryMinutes:
                return 'expired OTP Request Another one'
            if record.otp == otp:
                record.delete()
                return 'Done'
            else:
                return 'Wrong OTP'
        else:
            return 'No OTP Requested'

    def get(self, request):  # for checking otp
        self.refreshResponseDate()
        try:
            email = request.GET['email']
            otp = request.GET['otpToCheck']
            operation = request.GET['operation']
            if operation == 'register':
                response = self.checkOtp(email, otp)
                if response == 'Done':
                    self.responseData['message'] = 'Done'
                else:
                    self.responseData['message'] = response
            elif operation == 'forget password':
                user = User.objects.all().filter(email=email).first()
                response = self.checkOtp(email, otp)
                if response == 'Done' and user != None:
                    self.responseData['message'] = 'Done'
                    refreshedToken = RefreshToken.for_user(user)
                    self.responseData['access'] = str(
                        refreshedToken.access_token)
                else:
                    if user == None:
                        self.responseData['message'] = 'Not Valid Email'
                    else:
                        self.responseData['message'] = response
            else:
                self.responseData['message'] = 'Not Valid Operation'
        except Exception as ex:
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(self.responseData, safe=False)


class upgrade (AuthenticationAPIView):
    # this not useful in the delivery
    # will be developed in the next delivery
    pass


class updateData (AuthenticationAPIView):
    # using user serlializer and form submited
    # will be handeled later
    def dataChecker(self, data):
        if data.get('password') != None or data.get('username') != None or data.get('email') != None:
            return False
        else:
            return True

    def put(self, request):
        self.refreshResponseDate()
        if (not self.dataChecker(request.data)):
            self.responseData['message'] = 'Not Valid Data'
        else:
            ser = userUpdateSerializer(data=request.data)
            if ser.is_valid():
                response = ser.update(self.user, ser.validated_data)
                self.responseData['message'] = response['message']
            else:
                self.responseData['message'] = 'Not valid data'
        return JsonResponse(self.responseData, safe=False)


class changePass (AuthenticationAPIView):
    def put(self, request):
        # get the current password and the new password
        self.refreshResponseDate()
        currentPassword = request.POST.get('current')
        newPassword = request.POST.get('new')
        if currentPassword == None:
            user = User.objects.all().filter(email=request.POST.get('email')).first()
            user.set_password(newPassword)
            user.save()
            self.responseData['message'] = 'Done'
        else:
            if self.user.check_password(currentPassword):
                self.user.set_password(newPassword)
                self.user.save()
                self.responseData['message'] = 'Done'
                # can change the password
            else:
                self.responseData['message'] = 'Wrong Password'

        return JsonResponse(self.responseData, safe=False)


class forget (DefaultAPIView):
    # return the email of the query user
    # to send otp to the user
    def get(self, request):
        self.refreshResponseDate()
        username_or_email = request.GET['username_or_email']
        user = User.objects.all().filter(username=username_or_email).first()
        if user == None:
            user = User.objects.all().filter(email=username_or_email).first()
        if user == None:
            self.responseData['message'] = 'Note Valid Creditionals'
        else:
            self.responseData['message'] = user.email


class imageHandeller (DefaultAPIView):
    # this will be modified after deployment
    def perform_authentication(self, request):
        return None

    def get(self, request):
        self.refreshResponseDate()
        blocked_images = []
        path = request.GET.get('path')
        if (path == '' or path == None):
            return HttpResponse('')
        else:
            if str(path).split('/')[-1] in blocked_images:
                AuthenticationAPIView.perform_authentication(self, request)
            with open(settings.BASE_DIR / path, 'rb') as f:
                imageData = f.read()
            # return JsonResponse(self.responseData)
            return HttpResponse(imageData, content_type="image/png")


class userHandeler (DefaultAPIView):
    def get(self, request):
        self.refreshResponseDate()
        username = request.GET['username']
        basicUser = User.objects.all().filter(username=username).first()
        userData = user.objects.all().filter(user=basicUser).first()
        crewData = crew.objects.all().filter(member=userData).first()
        userDict = {
            'first_name': userData.user.first_name,
            'last_name': userData.user.last_name,
            'email': userData.user.email,
            'phone': userData.phone,
            'university': userData.university,
            'collage': userData.collage,
            'level': userData.level,
            'photo': userData.photo.photo.name,
            'gender': userData.gen,
        }
        if crewData != None:
            userDict['position'] = crewData.role
            userDict['rate'] = crewData.rate
        else:
            userDict['position'] = 'Participant'
        self.responseData['message'] = 'Done'
        self.responseData['user'] = userDict

        return JsonResponse(self.responseData, safe=False)


class userChecker (AuthenticationAPIView):
    def get(self, request):
        self.refreshResponseDate()
        if self.user.username == request.GET['username']:
            self.responseData['message'] = 'Yes'
        else:
            self.responseData['message'] = 'No'
        return JsonResponse(self.responseData, safe=False)


# how to handle images
# print(request.data)
# print(request.data['fdsafds'])
# img = Image.open(request.data['fdsafds'])
# print(img)
# img.show()
