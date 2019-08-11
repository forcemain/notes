#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf.urls import url


from . import views


app_name = 'cas_app'


urlpatterns = [
    url(r'request-token/$', views.cas_request_token_view, name='cas-request-token'),
    url(r'authorize/$', views.cas_user_authentication_view, name='cas-user-authentication'),
    url(r'verify-token/$', views.cas_token_verification_view, name='cas-token-verification'),
]
