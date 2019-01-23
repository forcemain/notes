#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


from .platform import Platform


class Trace(models.Model):
    TYPE_CHOICE_LOGIN = 0
    TYPE_CHOICE_LOGOUT = 1
    TYPE_CHOICE_MODIFY = 2
    TYPE_CHOICE_DELETE = 3

    TYPE_CHOICES = (
        (TYPE_CHOICE_LOGIN, _('login')),
        (TYPE_CHOICE_LOGOUT, _('logout')),
        (TYPE_CHOICE_MODIFY, _('modify')),
        (TYPE_CHOICE_DELETE, _('delete')),
    )

    type = models.SmallIntegerField(
        _('operation type'),
        choices=TYPE_CHOICES,
    )
    ctime = models.DateTimeField(
        _('create time'),
        auto_now_add=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='user',
        related_name='user_traces',
        blank=True, null=True,
    )
    platform = models.ForeignKey(
        Platform,
        verbose_name='platform',
        related_name='platform_traces',
        blank=True,
    )

    def get_user_name(self):
        return self.user.nickname or self.user.username or ''

    def __unicode__(self):
        return '{0}:{1}'.format(self.get_user_name(), self.get_type_display())
