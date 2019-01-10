#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import string


from os import urandom
from random import sample
from binascii import hexlify
from functools import partial
from django.conf import settings


def generate_random_token(num=20):
    return hexlify(urandom(num))


def generate_random_characters(init=string.letters, num=20):
    character_list = sample(init, num)

    return ''.join(character_list)


# generate random access key id
generate_random_ak = partial(generate_random_characters, init=string.uppercase, num=settings.ACCESS_KEY_LENGTH)
# generate random secret access key
generate_random_sk = partial(generate_random_characters, init=string.letters, num=settings.SECRET_ACCESS_KEY_LENGTH)
