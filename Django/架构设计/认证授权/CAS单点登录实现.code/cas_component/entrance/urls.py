#! -*- coding: utf-8 -*-


# author: forcemain@163.com


"""entrance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include
from cas_app.restapi.v1.urls import urlpatterns as cas_api_v1_urlpatterns


restv1_urls = []
restv1_urls.extend(cas_api_v1_urlpatterns)


urlpatterns = [
    url(r'^v1/', include((restv1_urls, 'restapi-v1'))),
]


urlpatterns += [
    url(r'^cas/', include('cas_app.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]


if settings.DEBUG is True:
    urlpatterns += [
        url(r'^v1/auth/', include('rest_framework.urls', namespace='rest_framework_auth')),
    ]
