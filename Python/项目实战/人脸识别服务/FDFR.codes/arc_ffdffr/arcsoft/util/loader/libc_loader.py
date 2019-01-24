#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ctypes import *
from arcsoft import settings
from arcsoft.data import SdkLoader


_sdk_reader = SdkLoader()


libc = cdll.msvcrt if _sdk_reader.system == 'wins' else CDLL(settings.LINUX_LIBC_NAME)
