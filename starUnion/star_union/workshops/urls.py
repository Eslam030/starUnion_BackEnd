from django.urls import path, include
from django.views import View
from .views import *


urlpatterns = [
    path('workshops/', workshop.as_view(), name='workshop'),
    path('instructor/', instructor.as_view(), name='instructor'),
    path('participant/', participant.as_view(), name='participant'),
    path('registerwork/', registerForWorkshop.as_view(), name='register_workshop'),
    path('accept/', acceptWorkshop.as_view(), name='accept_workshop'),

]
