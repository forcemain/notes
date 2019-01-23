#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.utils.decorators import classonlymethod
from django.contrib.auth.views import login_required


class LoginRequiredMixin(object):
    @classonlymethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)
