#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft.model.fr import AfrFsdkVersion


def func_get_version(library):
    wrapper = library.AFR_FSDK_GetVersion
    wrapper.restype = POINTER(AfrFsdkVersion)
    wrapper.argtypes = (c_void_p,)

    return wrapper
