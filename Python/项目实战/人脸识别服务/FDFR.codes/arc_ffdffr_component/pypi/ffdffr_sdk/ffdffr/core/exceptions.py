#! -*- coding: utf-8 -*-


# author: forcemain@163.com


class SdkException(Exception):
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message

    def __str__(self):
        return '<{0} code: {1} message: {2}>'.format(self.__class__.__name__, self.code, self.message)
