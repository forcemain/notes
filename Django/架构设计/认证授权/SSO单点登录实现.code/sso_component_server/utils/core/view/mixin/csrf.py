#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.views.decorators.csrf import csrf_exempt


class CsrfExemptMixin(object):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(CsrfExemptMixin, self).dispatch(*args, **kwargs)
