#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft.model.fd import AfdFsdkFaceres
from arcsoft.model import FsdkASVLOFFSCREEN


def func_still_image_detection(library):
    wrapper = library.AFD_FSDK_StillImageFaceDetection
    wrapper.restype = c_long
    wrapper.argtypes = (c_void_p, POINTER(FsdkASVLOFFSCREEN), POINTER(POINTER(AfdFsdkFaceres)))

    return wrapper
