from django.urls import path, include
from django.views import View
from .views import *


urlpatterns = [
    path('workshop/', workshop.as_view(), name='workshop'),
    path('registerwork/', registerForWorkshop.as_view(), name='register_workshop'),
    path('accept/', acceptWorkshop.as_view(), name='accept_workshop'),
    # path('workshops/', dummy.as_view(), name='workshops'),
    #
    # path('checkuser/', dummy.as_view(), name='checkUser_workshop')

]
