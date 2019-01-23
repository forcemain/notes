#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf.urls import url


from . import views


app_name = 'sso_app'


urlpatterns = [
    url(r'^authenticate/$', views.SSOAuthenticateView.as_view(), name='sso-authenticate'),
    url(r'^login/$', views.SSOLoginView.as_view(), name='sso-login'),
    url(r'^logout/$', views.SSOLogoutView.as_view(), name='sso-logout'),
]
