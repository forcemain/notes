#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf.urls import url


app_name = 'cas_app'


from . import views


urlpatterns = [
    url(r'^login/$', views.UserLoginView.as_view(), name='user-login'),
    url(r'^logout/$', views.UserLogoutView.as_view(), name='user-logout'),
    url(r'^weixin-login/$', views.WeixinUserLoginView.as_view(), name='user-weixin-login'),
    url(r'^weixin-authenticate', views.WeixinUserAuthenticateView.as_view() , name='user-weixin-authenticate'),
]
