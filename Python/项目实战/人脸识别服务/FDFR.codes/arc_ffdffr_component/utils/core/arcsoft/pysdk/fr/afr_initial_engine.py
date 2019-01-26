#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *


def func_initial_engine(library):
    wrapper = library.AFR_FSDK_InitialEngine
    wrapper.restype = c_long
    wrapper.argtypes = (c_char_p, c_char_p, c_void_p, c_int32, POINTER(c_void_p))

    return wrapper
