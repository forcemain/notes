#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.db import models
from django.utils.translation import ugettext_lazy as _


class Site(models.Model):
    url = models.URLField(
        _('site url'),
        unique=True,
    )
    ctime = models.DateTimeField(
        _('create time'),
        auto_now_add=True,
    )

    def __unicode__(self):
        return self.url
