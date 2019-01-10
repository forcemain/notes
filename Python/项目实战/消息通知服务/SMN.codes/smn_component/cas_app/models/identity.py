#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from utils.generator import generate_random_ak, generate_random_sk


class Identity(models.Model):
    access_key_id = models.CharField(
        _('access key id'),
        max_length=settings.ACCESS_KEY_LENGTH,
        blank=True,
        default=generate_random_ak
    )
    secret_access_key = models.CharField(
        _('secret access key'),
        max_length=settings.SECRET_ACCESS_KEY_LENGTH,
        blank=True,
        default=generate_random_sk
    )
    enable = models.BooleanField(
        _('enabled'),
        default=True,
        help_text=_('Designates whether the user can use the ak/sk.'),
    )
    create_time = models.DateTimeField(
        _('create time'),
        auto_now_add=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='identities',
        verbose_name=_('user')
    )

    class Meta:
        unique_together = (('access_key_id', 'secret_access_key'), )
        verbose_name = _('identity')
        verbose_name_plural = _('identities')

    def __unicode__(self):
        return '{0}:{1}'.format(self.user.username, self.access_key_id)
