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
    face_tracking_name = 'libarcsoft_fsdk_face_tracking'
    age_estimation_name = 'libarcsoft_fsdk_age_estimation'
    face_detection_name = 'libarcsoft_fsdk_face_detection'
    face_recognition_name = 'libarcsoft_fsdk_face_recognition'
    gender_estimation_name = 'libarcsoft_fsdk_gender_estimation'

    def __init__(self):
        self.system = platform.system()[0]
        self.x86_64 = '64bit' in platform.architecture()

    def _get_sdk_related_dir(self):
        _system_name = 'wins' if self.system == 'Windows' else 'linux'
        version_name = '64' if self.x86_64 else '32'

        return os.path.join(_system_name, version_name)

    def _get_sdk_dir(self):
        data_dir = get_data_dir()

        return os.path.join(data_dir, 'sdk', self._get_sdk_related_dir())

    def _get_sdk_path(self, name):
        return os.path.join(self._get_sdk_dir(), '{0}{1}'.format(name, self._get_sdk_ext()))

    def _get_sdk_ext(self):
        return '.dll' if self.system == 'Windows' else '.so'

    @property
    def face_tracking_path(self):
        return self._get_sdk_path(self.face_tracking_name)

    @property
    def age_estimation_path(self):
        return self._get_sdk_path(self.age_estimation_name)

    @property
    def face_detection_path(self):
        return self._get_sdk_path(self.face_detection_name)

    @property
    def gender_estimation_path(self):
        return self._get_sdk_path(self.gender_estimation_name)

    @property
    def face_recognition_path(self):
        return self._get_sdk_path(self.face_recognition_name)

