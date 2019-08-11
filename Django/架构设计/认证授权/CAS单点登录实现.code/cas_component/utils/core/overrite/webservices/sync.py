#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def provider_for_django(provider):
    def provider_view(request):
        def get_header(key, default):
            django_key = 'HTTP_%s' % key.upper().replace('-', '_')
            return request.META.get(django_key, default)
        method = request.method
        # Compatible with low version Django
        try:
            signed_data = request.raw_post_data
        except AttributeError:
            signed_data = request.body
        # if getattr(request, 'body', None):
        #     signed_data = request.body
        # else:
        #     signed_data = request.raw_post_data
        status_code, data = provider.get_response(
            method,
            signed_data,
            get_header,
        )
        return HttpResponse(data, status=status_code)
    return csrf_exempt(provider_view)
