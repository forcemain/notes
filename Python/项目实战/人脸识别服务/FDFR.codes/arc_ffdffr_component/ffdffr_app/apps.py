#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.apps import AppConfig


class FfdffrAppConfig(AppConfig):
    name = 'ffdffr_app'

    def ready(self):
        import ffdffr_app.signals
