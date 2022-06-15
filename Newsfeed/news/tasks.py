from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery import shared_task
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
import requests
from .views import upload_news, mailmethod

@shared_task
def update_news():
    upload_news()
    # mailmethod()
    


