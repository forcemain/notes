#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *


def func_uninitial_engine(library):
    wrapper = library.AFD_FSDK_UninitialFaceEngine
    wrapper.restype = c_long
    wrapper.argtypes = (c_void_p,)

    return wrapper
