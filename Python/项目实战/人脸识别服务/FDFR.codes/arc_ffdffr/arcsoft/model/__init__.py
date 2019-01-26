#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *


c_ubyte_p = POINTER(c_ubyte)


class SingleFace(object):
    def __init__(self, left=0, top=0, right=0, bottom=0, orient=0, image=None):
        self.left = left
        self.top = top
        self.image = image
        self.right = right
        self.orient = orient
        self.bottom = bottom


class FsdkMRECT(Structure):
    _fields_ = [
        ('left', c_int32),
        ('top', c_int32),
        ('right', c_int32),
        ('bottom', c_int32)
    ]


class FsdkASVLOFFSCREEN(Structure):
    _fields_ = [
        (u'u32PixelArrayFormat', c_uint32),
        (u'i32Width', c_int32),
        (u'i32Height', c_int32),
        (u'ppu8Plane', c_ubyte_p * 4),
        (u'pi32Pitch', c_int32 * 4)
    ]

    def __init__(self):
        Structure.__init__(self)

        self.gc_ppu8Plane0 = None
        self.gc_ppu8Plane1 = None
        self.gc_ppu8Plane2 = None
        self.gc_ppu8Plane3 = None
