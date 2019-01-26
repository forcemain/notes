#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft.model.fr import AfrFsdkFaceModel


def func_facepair_matching(library):
    wrapper = library.AFR_FSDK_FacePairMatching
    wrapper.restype = c_long
    wrapper.argtypes = (c_void_p, POINTER(AfrFsdkFaceModel), POINTER(AfrFsdkFaceModel), POINTER(c_float))

    return wrapper
