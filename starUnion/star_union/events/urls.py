from django.urls import path
from django.views import View


class dummy (View):
    pass


urlpatterns = [
    path('events/', dummy.as_view, name='events'),
    path('accept/', dummy.as_view, name='accept_event'),
    path('registerevent/', dummy.as_view, name='register_event')
]
