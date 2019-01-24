#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import logging


from ctypes import *


# Base
APP_ID = c_char_p(b'')
SDK_KEY = c_char_p(b'')

# Libc
LINUX_LIBC_NAME = 'libc.so.6'


# Logging
DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(pathname)s - %(lineno)d - %(levelname)s - %(message)s'
