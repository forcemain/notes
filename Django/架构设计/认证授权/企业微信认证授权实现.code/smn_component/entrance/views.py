#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib.auth import get_user
from django.shortcuts import render
from django.contrib.sessions.models import Session


# @login_required
def home(request):
    request.user = get_user(request)
    return render(request, 'entrance/home.html')
