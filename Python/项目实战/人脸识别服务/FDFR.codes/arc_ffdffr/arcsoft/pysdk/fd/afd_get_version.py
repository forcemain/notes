#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft.model.fd import AfdFsdkVersion


def func_get_version(library):
    wrapper = library.AFD_FSDK_GetVersion
    wrapper.restype = POINTER(AfdFsdkVersion)
    wrapper.argtypes = (c_void_p,)

    return wrapper
