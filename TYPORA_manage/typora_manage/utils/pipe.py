#! -*- coding: utf-8 -*-


# author: forcemain@163.com


class Pipe(object):
    def __init__(self, func):
        self.func = func

    def __ror__(self, other):
        return self.func(other)

    def __call__(self, *args, **kwargs):
        return Pipe(lambda r: self.func(r, *args, **kwargs))
