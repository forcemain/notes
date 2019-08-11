#! -*- coding: utf-8 -*-


# author: forcemain@163.com

from django.db import models
from django.conf import settings
from django.utils import timezone
from utils.generator import generate_random_key
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class KeyGenerator(object):
    def __init__(self, field, key_length=64):
        self.field = field
        self.key_length = key_length

    def get_model(self):
        raise NotImplementedError

    def was_key_exist(self, key):
        return self.get_model().objects.filter(**{self.field: key}).exists()

    def __call__(self, *args, **kwargs):
        key = generate_random_key(self.key_length)
        while self.was_key_exist(key):
            key = generate_random_key(self.key_length)
        return key


@deconstructible
class SecretKeyGenerator(KeyGenerator):
    def get_model(self):
        return CasConsumer


@deconstructible
class AccessKeyGenerator(KeyGenerator):
    def get_model(self):
        return CasConsumer


@deconstructible
class CasTokenGenerator(KeyGenerator):
    def get_model(self):
        return CasToken


class CasConsumer(models.Model):
    name = models.CharField(
        _('name'),
        max_length=255, unique=True,
    )
    access_key = models.CharField(
        _('access key'),
        max_length=settings.ACCESS_KEY_LENGTH,
        default=AccessKeyGenerator('access_key', settings.ACCESS_KEY_LENGTH)
    )
    secret_key = models.CharField(
        _('secret key'),
        max_length=settings.SECRET_KEY_LENGTH,
        default=SecretKeyGenerator('secret_key', settings.SECRET_KEY_LENGTH)
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('cas consumer')
        verbose_name_plural = _('cas consumers')


class CasToken(models.Model):
    access_token = models.CharField(
        _('access token'),
        unique=True, max_length=settings.CAS_ACCESS_TOKEN_LENGTH,
        default=CasTokenGenerator('access_token', settings.CAS_ACCESS_TOKEN_LENGTH)
    )
    request_token = models.CharField(
        _('request token'),
        unique=True, max_length=settings.CAS_REQUEST_TOKEN_LENGTH,
        default=CasTokenGenerator('request_token', settings.CAS_REQUEST_TOKEN_LENGTH)
    )
    timestamp = models.DateTimeField(
        _('timestamp'),
        default=timezone.now
    )
    redirect_to = models.CharField(
        _('redirect to'),
        max_length=255
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE
    )

    cas_consumer = models.ForeignKey(
        CasConsumer,
        related_name='cas_tokens',
        verbose_name=_('cas consumer'),
        on_delete=models.CASCADE
    )

    def refresh(self):
        self.timestamp = timezone.now()
        self.save()

    def __unicode__(self):
        return '{0} ({1})'.format(self.redirect_to, self.cas_consumer.name)

    class Meta:
        verbose_name = _('cas token')
        verbose_name_plural = _('cas tokens')
