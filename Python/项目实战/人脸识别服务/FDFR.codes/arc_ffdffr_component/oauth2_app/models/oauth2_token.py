#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class OAuth2Token(models.Model):
    token = models.CharField(
        _('oauth2 token'),
        max_length=128,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='user',
        related_name='user_oauth2_tokens',
    )
    endpoint = models.URLField(
        _('oauth2 server endpoint'),
    )

    class Meta:
        unique_together = ('token', 'endpoint')
        verbose_name = _('oauth2 token')
        verbose_name_plural = _('oauth2 tokens')

    def __unicode__(self):
        return '{0}({1})'.format(self.token, self.endpoint)
