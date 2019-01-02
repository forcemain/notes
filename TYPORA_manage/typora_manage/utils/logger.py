#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import logging


from typora_manage import settings


class Logger(object):
    def __init__(self, **kwargs):
        _level = kwargs.get('level', settings.DEFAULT_LOG_LEVEL)
        _format = kwargs.get('format', settings.DEFAULT_LOG_FORMAT)

        logging.basicConfig(level=_level, format=_format)

    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)
