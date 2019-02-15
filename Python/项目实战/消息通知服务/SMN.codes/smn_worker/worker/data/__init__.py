#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os


def get_base_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_worker_dir():
    return os.path.dirname(get_base_dir())


def get_project_dir():
    return os.path.dirname(get_worker_dir())
