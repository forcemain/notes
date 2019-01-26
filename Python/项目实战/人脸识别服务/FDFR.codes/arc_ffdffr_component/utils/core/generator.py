#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os
import binascii


def generate_key(num=32):
    return binascii.hexlify(os.urandom(num/2))
