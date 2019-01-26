#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *


def func_uninitial_engine(library):
    wrapper = library.AFR_FSDK_UninitialEngine
    wrapper.restype = c_long
    wrapper.argtypes = (c_void_p,)

    return wrapper
