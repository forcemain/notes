#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Session(models.Model):
    session_key = models.CharField(
        _('session key'),
        max_length=64,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='user',
        related_name='user_sessions',
    )
    ctime = models.DateTimeField(
        _('create time'),
        auto_now_add=True,
    )
    mtime = models.DateTimeField(
        _('modify time'),
        auto_now=True,
    )

    def __unicode__(self):
        return '{0}:{1}'.format(self.session_key, self.mtime)


