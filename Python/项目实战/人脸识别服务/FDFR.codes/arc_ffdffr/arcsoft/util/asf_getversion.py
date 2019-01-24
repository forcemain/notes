#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft.core.structure import ASFVersion
from arcsoft.util.loader.engine_loader import engine


func_asf_getversion = engine.ASFGetVersion
func_asf_getversion.restype = POINTER(ASFVersion)
func_asf_getversion.argtypes = (c_void_p,)

