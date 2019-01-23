#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from django.db import models
from django.utils.translation import ugettext_lazy as _


class Platform(models.Model):
    ip = models.GenericIPAddressField(
        _('ip address'),
    )
    location = models.CharField(
        _('location'),
        max_length=64, blank=True,
    )
    endpoint = models.CharField(
        _('endpoint'),
        max_length=200, blank=True,
    )
    ctime = models.DateTimeField(
        _('create time'),
        auto_now_add=True,
    )

    def __unicode__(self):
        return '{0}:{1}'.format(self.location, self.ip)
