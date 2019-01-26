#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.apps import AppConfig


class Oauth2AppConfig(AppConfig):
    name = 'oauth2_app'

    def ready(self):
        import oauth2_app.signals
