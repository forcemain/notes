#! -*- coding: utf-8 -*-


# author: forcemain@163.com

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


UserModel = get_user_model()


class WeixinUser(UserModel):
    class Meta:
        verbose_name = _('weixin user')
        verbose_name_plural = _('weixin users')

    def __unicode__(self):
        return '{0}({1})'.format(self.username, self.date_joined)
