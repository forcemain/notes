#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.apps import AppConfig


class CasAppConfig(AppConfig):
    name = 'cas_app'

    def ready(self):
        import cas_app.signals
