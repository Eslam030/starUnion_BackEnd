from django.urls import path
from .views import *

app_name = 'events'
urlpatterns = [
    path('events/', events.as_view(), name='events'),  # to get or create events
    path('registerevent/', registerForEvent.as_view(),
         name='register_event'),  # to register a user for an event
    # to get or create sponsors
    path('sponsors/', sponsors.as_view(), name='events'),
    # to get or create parteners
    path('partners/', partners.as_view(), name='events'),
    path('addeventsponsor/', sponsorsEvents.as_view(),
         name='addeventsponsor'),  # to add sponsors to events
    path('addpartenersponsor/', partnerSponsoringEvents.as_view(),  # to add parteners as a sponsor to events
         name='addpartenersponsor')
]
