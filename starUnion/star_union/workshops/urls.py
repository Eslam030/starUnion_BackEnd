from django.urls import path, include
from django.views import View
from .views import *


# add end point for top 5 in specific workshop
app_name = 'workshops'
urlpatterns = [
    path('workshops/', workshop.as_view(), name='workshop'),
    path('instructors/', instructor.as_view(), name='instructor'),
    path('participant/', participant.as_view(), name='participant'),
    path('registerwork/', registerForWorkshop.as_view(), name='register_workshop'),
    path('accept/', acceptWorkshop.as_view(), name='accept_workshop'),
    path('top5/', top5.as_view(), name='top5')
]
