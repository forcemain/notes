#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import hashlib


def gen_strs_md5(data):
    return hashlib.md5(data).hexdigest()
