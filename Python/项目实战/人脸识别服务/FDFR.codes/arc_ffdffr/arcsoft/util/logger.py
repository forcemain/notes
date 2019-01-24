#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import logging


class Logger(object):
    @staticmethod
    def get_logger(name):
        return logging.getLogger(name)
