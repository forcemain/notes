#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_with_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
