#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft.data import SdkLoader


_sdk_reader = SdkLoader()


helper = CDLL(_sdk_reader.helper_path)
engine = CDLL(_sdk_reader.engine_path)
