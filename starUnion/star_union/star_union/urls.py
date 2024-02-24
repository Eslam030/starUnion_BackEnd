from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('/', include('routing.urls')),
    path('main/', include('main.urls')),
    path('event/', include('events.urls')),
    path('workshop/', include('workshops.urls')),
    path('admin/', admin.site.urls)
]
