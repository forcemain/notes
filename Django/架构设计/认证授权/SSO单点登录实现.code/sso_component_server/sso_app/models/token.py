#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from django.db import models
from django.conf import settings
from utils.generator import generate_random_key
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


from .site import Site


@deconstructible
class GenerateRandomKey(object):
    def __init__(self, field, max_length=settings.SSO_TOKEN_KEY_LENGTH):
        self.field = field
        self.max_length = max_length

    def get_model(self):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        random_key = generate_random_key(self.max_length)
        while self.get_model().objects.filter(**{self.field: random_key}).exists():
            random_key = generate_random_key(self.max_length)

        return random_key


@deconstructible
class GenerateSSOTokenKey(GenerateRandomKey):
    def get_model(self):
        return Token


class Token(models.Model):
    access_token = models.CharField(
        _('user access token'),
        max_length=settings.SSO_TOKEN_KEY_LENGTH,
        default=GenerateSSOTokenKey('access_token')
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name='user',
        related_name='user_token',
        blank=True,
    )
    ctime = models.DateTimeField(
        _('create time'),
        auto_now_add=True,
    )
    mtime = models.DateTimeField(
        _('modify time'),
        auto_now=True,
    )

    def refresh(self):
        self.access_token = GenerateSSOTokenKey('access_token')()
        self.save()

    def __unicode__(self):
        return '{0}:{1}'.format(self.access_token, self.mtime)

