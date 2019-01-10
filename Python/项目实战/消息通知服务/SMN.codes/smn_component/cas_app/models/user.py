#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    nickname = models.CharField(
        _('nick name'),
        max_length=50, blank=True,
    )

    class Meta(AbstractUser.Meta):
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return '{0}({1})'.format(self.username, self.nickname) if self.nickname else self.username
