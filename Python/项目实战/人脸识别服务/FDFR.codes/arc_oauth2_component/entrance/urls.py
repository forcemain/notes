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


from django.contrib import admin
from django.conf import settings
from django.http import JsonResponse
from django.views.static import serve
from django.conf.urls import url, include
from oauth2_app.restapi.v1.urls import urlpatterns as oauth2_api_v1_urlpatterns


restv1_urls = []
restv1_urls.extend(oauth2_api_v1_urlpatterns)


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2-provider')),
]

urlpatterns += [
    url(r'^v1/', include((restv1_urls, 'restapi-v1'))),
]

if settings.DEBUG is True:
    urlpatterns += [
        url(r'^medias/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        url(r'^v1/auth/', include('rest_framework.urls', namespace='rest_framework_auth'))
    ]

urlpatterns += [
    url(r'', lambda request: JsonResponse({'service': 'arc_oauth2_component', 'version': '1.0'}), name='service'),
]
