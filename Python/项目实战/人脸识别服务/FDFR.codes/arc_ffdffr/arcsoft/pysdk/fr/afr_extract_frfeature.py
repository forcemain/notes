#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft.model import FsdkASVLOFFSCREEN
from arcsoft.model.fr import AfrFsdkFaceInput, AfrFsdkFaceModel


def func_extract_frfeature(library):
    wrapper = library.AFR_FSDK_ExtractFRFeature
    wrapper.restype = c_long
    wrapper.argtypes = (c_void_p, POINTER(FsdkASVLOFFSCREEN), POINTER(AfrFsdkFaceInput), POINTER(AfrFsdkFaceModel))

    return wrapper
