#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from cas_app import models
from django.contrib.auth.backends import AllowAllUsersRemoteUserBackend


UserModel = models.WeixinUser


class WeixinQcodeRemoteUserBackend(AllowAllUsersRemoteUserBackend):
    def authenticate(self, request, remote_user):
        return super(WeixinQcodeRemoteUserBackend, self).authenticate(request, remote_user)
