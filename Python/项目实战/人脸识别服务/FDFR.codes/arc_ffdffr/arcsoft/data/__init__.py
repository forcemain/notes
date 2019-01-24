#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os
import platform


def get_data_dir():
    return os.path.dirname(__file__)


def get_arcsoft_dir():
    return os.path.dirname(get_data_dir())


def get_project_dir():
    return os.path.dirname(get_arcsoft_dir())


class SdkLoader(object):
    HELPER_NAME = 'libarcsoft_face'
    ENGINE_NAME = 'libarcsoft_face_engine'

    def __init__(self):
        self.system = platform.system()[0]
        self.x86_64 = '64bit' in platform.architecture()

    def _get_sdk_related_path(self):
        _system_name = 'wins' if self.system == 'Windows' else 'linux'
        version_name = '64' if self.x86_64 else '32'

        return os.path.join(_system_name, version_name)

    def _get_sdk_path(self):
        data_dir = get_data_dir()

        return os.path.join(data_dir, 'sdk', self._get_sdk_related_path())

    def _get_sdk_ext(self):
        return '.dll' if self.system == 'Windows' else '.so'

    @property
    def helper_path(self):
        return os.path.join(self._get_sdk_path(), '{0}{1}'.format(self.HELPER_NAME, self._get_sdk_ext()))

    @property
    def engine_path(self):
        return os.path.join(self._get_sdk_path(), '{0}{1}'.format(self.ENGINE_NAME, self._get_sdk_ext()))
