#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns


from . import views


router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('groups', views.GroupViewSet)


urlpatterns = format_suffix_patterns([])
urlpatterns.extend(router.urls)
