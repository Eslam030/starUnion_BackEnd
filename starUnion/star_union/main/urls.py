from django.urls import path, include
from django.views import View
from main.views import *

app_name = 'main'
urlpatterns = [
    path('login/', login.as_view(), name='login'),
    path('user/', userHandeler.as_view(), name='user'),
    path('register/', register.as_view(), name='register'),
    path('checkuser/', register.as_view(), name='check_user'),
    path('test/', test.as_view(), name='test'),
    path('logout/', logout.as_view(), name='logout'),
    path('otpcheck/', otp.as_view(), name='check_otp'),
    path('sendotp/', otp.as_view(), name='send_otp'),
    path('upgrade/', upgrade.as_view(), name='user_upgrade'),
    path('changepass/', changePass.as_view(), name='change_password'),
    path('updateData/', updateData.as_view(), name='updateData'),
    path('getImage/', imageHandeller.as_view(), name='imageHandeller'),
    path('userForChange/', userChecker.as_view(), name='userChecker'),
    path('forget/', forget.as_view(), name='forget')
]
