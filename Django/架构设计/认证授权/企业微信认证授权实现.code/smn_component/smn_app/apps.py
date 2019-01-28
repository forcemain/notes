#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.apps import AppConfig


class SmnAppConfig(AppConfig):
    name = 'smn_app'

    def ready(self):
        from smn_app import signals
