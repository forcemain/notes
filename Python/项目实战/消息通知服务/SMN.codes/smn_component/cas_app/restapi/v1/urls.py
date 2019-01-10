#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns


from . import views


router = DefaultRouter()
router.register('identifies', views.IdentifyModelViewSet, base_name='identifies')


urlpatterns = format_suffix_patterns([])
urlpatterns.extend(router.urls)
