from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.urls import re_path

urlpatterns = [
    path('main/', include('main.urls', namespace='main')),
    path('event/', include('events.urls', namespace='events')),
    path('workshop/', include('workshops.urls', namespace='workshops')),
    path('admin/', admin.site.urls),
    path('home/', include('routing.urls', namespace='routing')),
]
