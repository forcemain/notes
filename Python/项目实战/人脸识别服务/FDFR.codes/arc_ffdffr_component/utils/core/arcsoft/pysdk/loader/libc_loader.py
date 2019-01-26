#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft import settings
from arcsoft.data import SdkLoader


_sdk_reader = SdkLoader()


libc = cdll.msvcrt if _sdk_reader.system == 'wins' else CDLL(settings.LINUX_LIBC_NAME)

libc.free.restype = None
libc.free.argtypes = (c_void_p,)
libc.malloc.restype = c_void_p
libc.malloc.argtypes = (c_size_t,)
libc.memcpy.restype = c_void_p
libc.memcpy.argtypes = (c_void_p, c_void_p, c_size_t)
