from django.urls import path, include
from django.views import View


class dummy (View):
    pass


urlpatterns = [
    path('registerwork/', dummy.as_view(), name='register_workshop'),
    path('workshops/', dummy.as_view(), name='workshops'),
    path('accept/', dummy.as_view(), name='accept_workshop'),
    path('checkuser/', dummy.as_view(), name='checkUser_workshop')
]
