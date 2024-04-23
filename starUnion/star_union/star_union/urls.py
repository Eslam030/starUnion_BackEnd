from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('/', include('routing.urls')),
    path('main/', include('main.urls')),
    path('event/', include('events.urls')),
    path('workshop/', include('workshops.urls')),
    path('admin/', admin.site.urls),
    path("", TemplateView.as_view(template_name="index.html")),
]
