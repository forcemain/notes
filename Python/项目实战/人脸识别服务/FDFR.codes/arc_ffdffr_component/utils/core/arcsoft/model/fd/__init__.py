#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft.model import FsdkMRECT


class AfdFsdkFaceres(Structure):
    _fields_ = [
        ('nFace', c_int32),
        ('rcFace', POINTER(FsdkMRECT)),
        ('lfaceOrient', POINTER(c_int32))
    ]


class AfdFsdkVersion(Structure):
    _fields_ = [
        ('lCodebase', c_int32),
        ('lMajor', c_int32),
        ('lMinor', c_int32),
        ('lBuild', c_int32),
        ('Version', c_char_p),
        ('BuildDate', c_char_p),
        ('CopyRight', c_char_p)
    ]
