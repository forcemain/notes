#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return '{0}({1})'.format(self.username, self.date_joined)
