#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import sys


from typora_manage.db import get_manage_dir
from typora_manage.core.management import execute_from_command_line


sys.path.insert(0, get_manage_dir())


if __name__ == '__main__':
    execute_from_command_line(sys.argv)
