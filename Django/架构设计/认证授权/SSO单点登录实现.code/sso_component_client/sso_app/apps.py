#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.apps import AppConfig


class SsoAppConfig(AppConfig):
    name = 'sso_app'

    def ready(self):
        from sso_app import signals
