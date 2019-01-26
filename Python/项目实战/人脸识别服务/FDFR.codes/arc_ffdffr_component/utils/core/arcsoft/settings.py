#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import logging


from ctypes import *


# Trace
TRACE_EXCEPTION = True

# Libc
LINUX_LIBC_NAME = 'libc.so.6'

# Fd
FD_WORK_BUFFER_SIZE = 20 * 1024 * 1024

# Fr
FR_WORK_BUFFER_SIZE = 40 * 1024 * 1024

# Base
APP_ID = c_char_p(b'BR5BjsNmV9YTWtudMckG6v2obKSzZB4fXWrB72K28RYf')
FD_KEY = c_char_p(b'C26tCwENbcKPTkU72D6QbeMY2ZBBR96qJAZtvyisc2dD')
FT_KEY = c_char_p(b'C26tCwENbcKPTkU72D6QbeMQs9uxb8m5z8ucvBqvKS8L')
FR_KEY = c_char_p(b'C26tCwENbcKPTkU72D6QbeN2gADoePL7AJSvFDKTiff7')
UA_KEY = c_char_p(b'C26tCwENbcKPTkU72D6QbeNGzxkAUE3K9PcJ73ZssThz')
UG_KEY = c_char_p(b'C26tCwENbcKPTkU72D6QbeNQAN1Ntiw2Ex73fZxPeU9X')

# Logging
DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(pathname)s - %(lineno)d - %(levelname)s - %(message)s'
