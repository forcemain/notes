#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft.model import FsdkMRECT
from arcsoft.pysdk.loader.libc_loader import libc


class AfrFsdkFaceInput(Structure):
    _fields_ = [
        ('rcFace', FsdkMRECT),
        ('lOrient', c_int32)
    ]


class AfrFsdkFaceModel(Structure):
    _fields_ = [
        ('pbFeature', c_void_p),
        ('lFeatureSize', c_int32)
    ]

    def __init__(self):
        Structure.__init__(self)

        self.bAllocByMalloc = False

    def __del__(self):
        self.free()

    def free(self):
        if self.bAllocByMalloc and self.pbFeature != 0:
            libc.free(self.pbFeature)
            self.pbFeature = 0

    def deepcopy(self):
        feature = AfrFsdkFaceModel()
        feature.bAllocByMalloc = True
        feature.lFeatureSize = self.lFeatureSize
        feature.pbFeature = libc.malloc(feature.lFeatureSize)
        libc.memcpy(feature.pbFeature, self.pbFeature, feature.lFeatureSize)

        return feature

    def to_bytearray(self):
        feature = create_string_buffer(self.lFeatureSize)
        libc.memcpy(cast(feature, c_void_p), self.pbFeature, self.lFeatureSize)

        return bytearray(feature)

    def from_bytearray(self, bytearray_feature):
        feature_data = create_string_buffer(bytearray_feature)
        feature = AfrFsdkFaceModel()
        feature.lFeatureSize = len(bytearray_feature)
        feature.bAllocByMalloc = True
        feature.pbFeature = libc.malloc(feature.lFeatureSize)
        libc.memcpy(feature.pbFeature, cast(feature_data, c_void_p), feature.lFeatureSize)

        return feature


class AfrFsdkVersion(Structure):
    _fields_ = [
        ('lCodebase', c_int32),
        ('lMajor', c_int32),
        ('lMinor', c_int32),
        ('lBuild', c_int32),
        ('lFeatureLevel', c_int32),
        ('Version', c_char_p),
        ('BuildDate', c_char_p),
        ('CopyRight', c_char_p)
    ]
