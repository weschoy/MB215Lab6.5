from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from sms.views import SMSView

urlpatterns = [
    url(r'^$', csrf_exempt(SMSView.as_view()))
]