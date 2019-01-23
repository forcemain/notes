#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Token(models.Model):
    access_token = models.CharField(
        _('user access token'),
        max_length=settings.SSO_TOKEN_KEY_LENGTH,
        blank=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='user',
        related_name='user_tokens',
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
        return '{0}:{1}'.format(self.access_token, self.mtime)

