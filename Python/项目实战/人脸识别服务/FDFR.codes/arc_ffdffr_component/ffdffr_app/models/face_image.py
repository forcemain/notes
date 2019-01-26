#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os


from django.db import models
from django.conf import settings
from django.utils import timezone
from utils.core.generator import generate_key
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class Uploader(object):
    def __init__(self, field, basedir):
        self.field = field
        self.basedir = basedir

    def get_model(self):
        raise NotImplementedError

    def __call__(self, instance, filename):
        now = timezone.now()
        key = generate_key()
        field = '{0}__contains'.format(self.field)
        while self.get_model().objects.filter(**{field: key}).exists():
            key = generate_key()
        return os.path.join(self.basedir, instance.user.username, str(now.year), str(now.month), str(now.day), key)


@deconstructible
class FaceImageUploader(Uploader):
    def get_model(self):
        return FaceImage


class FaceImage(models.Model):
    image = models.ImageField(
        _('face image'),
        upload_to=FaceImageUploader(field='image', basedir='face_images')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='user',
        related_name='user_face_images',
        blank=True, null=True,
    )
    ctime = models.DateTimeField(
        _('create time'),
        auto_now=True,
    )

    class Meta:
        verbose_name = 'face image'
        verbose_name_plural = 'face images'

    def __unicode__(self):
        return '{0}({1})'.format(self.user, self.image)
