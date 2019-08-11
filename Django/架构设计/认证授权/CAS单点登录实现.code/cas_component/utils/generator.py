#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from os import urandom
from binascii import hexlify


def generate_random_key(num=32):
    return hexlify(urandom(num/2))
