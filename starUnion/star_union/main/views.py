from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializer import userLoginSerializer, userSerializer
from .models import user_refresh_token, BlackListed, optData, user, user_profile_images
from django.http import JsonResponse, HttpResponse
import json
from django.conf import settings
from jwt import PyJWS
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
# this custom APIView for classes that
# i want to handle the expiration of the token i a custom way
# not just raise Not authentication Exception when it is expired


class DefaultAPIView (APIView):
    responseData = {}


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
        except Exception as ex:
            raise exceptions.NotAuthenticated

# done


class login (DefaultAPIView):
    def post(self, request):
        self.responseData = {}
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
        self.responseData['message'] = 'done'
        record = BlackListed()
        record.user = self.user
        record.save()
        return JsonResponse(self.responseData, safe=False)


class register (DefaultAPIView):
    def post(self, request):
        self.responseData = {}
        # get the data from the request
        ser = userSerializer(data=request.data)
        if ser.is_valid():
            response = ser.create(ser.validated_data)
            self.responseData['message'] = response['message']
        else:
            self.responseData['message'] = 'Not valid data'
        return JsonResponse(self.responseData, safe=False)
    # using user serlializer and form submited


class test (AuthenticationAPIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        if self.updatedTokenAccess != None:
            return JsonResponse({'message': 'Done', 'access': self.updatedTokenAccess, 'modified': 'done'})
        else:
            return JsonResponse({'message': 'Done'})


class otp (DefaultAPIView):
    otp_duration_in_minutes = 3

    def post(self, request):  # for sending otp
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

    def get(self, request):  # for checking otp
        email = request.GET['email']
        otp = request.GET['otpToCheck']
        record = optData.objects.all().filter(email=email).first()
        if record != None:
            currentDate = datetime.datetime.now(pytz.timezone('Africa/Cairo'))
            delta = currentDate - record.initTime
            datla = delta.total_seconds() / 60
            exipryMinutes = datetime.timedelta(
                minutes=self.otp_duration_in_minutes)
            if delta > exipryMinutes:
                return JsonResponse({'message': 'expired OTP Request Another one'})
            if record.otp == otp:
                record.delete()
                return JsonResponse({'message': 'Done'})
            else:
                return JsonResponse({'message': 'Wrong OTP'})
        else:
            return JsonResponse({'message': 'Request OTP'})


class upgrade (AuthenticationAPIView):
    # this not useful in the delivery
    # will be developed in the next delivery
    pass


class updateData (AuthenticationAPIView):
    # using user serlializer and form submited
    # will be handeled later
    def put(self, request):
        ser = userSerializer(data=request.data)
        if ser.is_valid():
            response = ser.update(self.user, ser.validated_data)
            self.responseData['message'] = response['message']
        return JsonResponse(self.responseData, safe=False)


class changePass (AuthenticationAPIView):
    def put(self, request):
        # get the current password and the new password
        currentPassword = request.POST['current']
        newPassword = request.POST['new']
        if self.user.check_password(currentPassword):
            self.user.set_password(newPassword)
            self.user.save()
            # can change the password
            return JsonResponse({'message': 'Done'})
        else:
            return JsonResponse({'message': 'Wrong Password'})


class imageHandeller (DefaultAPIView):
    # this will be modified after deployment
    def perform_authentication(self, request):
        return None

    def get(self, request):
        blocked_images = []
        path = request.GET.get('path')
        if str(path).split('/')[-1] in blocked_images:
            AuthenticationAPIView.perform_authentication(self, request)
        with open(settings.BASE_DIR / path, 'rb') as f:
            imageData = f.read()
        # return JsonResponse(self.responseData)
        return HttpResponse(imageData, content_type="image/png")


class userHandeler (AuthenticationAPIView):
    def get(self, request):
        userData = user.objects.all().filter(user=self.user).first()
        userDict = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'email': self.user.email,
            'phone': userData.phone,
            'university': userData.university,
            'collage': userData.collage,
            'level': userData.level,
            'photo': userData.photo.photo.path
        }
        self.responseData['message'] = 'Done'
        self.responseData['user'] = userDict

        return JsonResponse(self.responseData, safe=False)
# how to handle images
# print(request.data)
# print(request.data['fdsafds'])
# img = Image.open(request.data['fdsafds'])
# print(img)
# img.show()
