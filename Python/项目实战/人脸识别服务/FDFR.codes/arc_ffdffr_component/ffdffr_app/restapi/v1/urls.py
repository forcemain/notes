#! -*- coding: utf-8 -*-


# author: forcemain@163.com



from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns


from . import views


app_name = 'ffdffr_app'


router = DefaultRouter()


urlpatterns = format_suffix_patterns([
    url(r'^face/feature/$', views.FaceFeatureViewSet.as_view({'post': 'create'}), name='face-feature'),
])
urlpatterns.extend(router.urls)
