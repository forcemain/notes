#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft.util.loader.engine_loader import engine


func_asf_initengine = engine.ASFInitEngine
func_asf_initengine.restype = c_int32
func_asf_initengine.argtypes = (c_long, c_int32, c_int32, c_int32, c_int32, POINTER(c_void_p))
