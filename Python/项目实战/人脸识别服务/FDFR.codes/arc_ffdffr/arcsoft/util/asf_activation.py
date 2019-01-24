#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft.util.loader.engine_loader import engine


func_asf_activation = engine.ASFActivation
func_asf_activation.restype = c_int32
func_asf_activation.argtypes = (c_char_p, c_char_p)
