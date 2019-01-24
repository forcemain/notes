#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *


class ASFVersion(Structure):
    _fields_ = [
        ('Version', c_char_p),
        ('BuildDate', c_char_p),
        ('CopyRight', c_char_p)
    ]


class ASFSingleFaceRect(Structure):
    _fields_ = [
        ('left', c_int32),
        ('top', c_int32),
        ('right', c_int32),
        ('bottom', c_int32)
    ]


class ASFSingleFaceInfo(Structure):
    _fields_ = [
        ('faceRect', ASFSingleFaceRect),
        ('faceOrient', c_int32)
    ]


class ASFMultipleFaceInfo(Structure):
    _fields_ = [
        ('faceRect', POINTER(ASFSingleFaceRect)),
        ('faceOrient', POINTER(c_int32)),
        ('faceNum', c_int32)
    ]


class ASFSingleFaceFeature(Structure):
    _fields_ = [
        ('feature', POINTER(c_void_p)),
        ('featureSize', c_int32)
    ]


class ASFMultipleAgeInfo(Structure):
    _fields_ = [
        ('ageArray', POINTER(c_int32)),
        ('num', c_int32)
    ]


class ASFMultipleGenderInfo(Structure):
    _fields_ = [
        ('genderArray', POINTER(c_int32)),
        ('num', c_int32)
    ]
