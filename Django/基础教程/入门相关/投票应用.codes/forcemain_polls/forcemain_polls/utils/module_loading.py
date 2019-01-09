#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os
import imp
import importlib


def import_sub_module(package, name):

    try:
        m = importlib.import_module(package)
        path = m.__path__
    except AttributeError:
        return

    try:
        imp.find_module(name, path)
    except ImportError:
        return

    dotted_path = '{0}.{1}'.format(package, name)
    return importlib.import_module(dotted_path)


def autodiscovery_modules(package, entrance):
    modules = []

    cur_dir = os.path.dirname(entrance)
    pyfiles = os.listdir(cur_dir)

    for f_name in pyfiles:
        f_path = os.path.join(cur_dir, f_name)
        if os.path.isfile(f_path):
            if not f_name.endswith('.py'):
                continue
            m_name, _, _ = f_name.rpartition('.')
            if m_name == '__init__':
                continue
        else:
            m_name = f_name

        m = import_sub_module(package, m_name)
        if not m:
            continue
        modules.append(m)
    return modules
