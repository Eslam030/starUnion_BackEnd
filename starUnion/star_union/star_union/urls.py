from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.urls import re_path

urlpatterns = [
    path('main/', include('main.urls')),
    path('event/', include('events.urls')),
    path('workshop/', include('workshops.urls')),
    path('admin/', admin.site.urls),
    path('home/', include('routing.urls')),
]
