#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib.auth.views import LoginView, LogoutView


class UserLoginView(LoginView):
    template_name = 'cas_app/user/login.html'


class UserLogoutView(LogoutView):
    pass
