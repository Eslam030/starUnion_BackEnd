from django.urls import path, include, re_path
from django.views.generic import TemplateView

app_name = 'routing'
urlpatterns = [
    re_path(r'^.*$',
            TemplateView.as_view(template_name='base.html')),
]
