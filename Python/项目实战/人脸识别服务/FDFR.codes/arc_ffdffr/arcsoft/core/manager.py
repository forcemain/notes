#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import os
import cv2
import numpy
import logging
from PIL import Image


from ctypes import *
from arcsoft import settings
from arcsoft.util.logger import Logger


logger = Logger.get_logger(__file__)


class BaseManager(object):
    handle = c_void_p()


class RLSBManager(BaseManager):
    def __init__(self, app_id=None, sdk_key=None, debug=True):
        self.debug = debug
        self.app_id = app_id or settings.APP_ID
        self.sdk_key = sdk_key or settings.SDK_KEY

        self.do_asf_setup()

    def do_asf_setup(self):
        if not self.debug:
            return
        logging.basicConfig(level=settings.DEFAULT_LOG_LEVEL, format=settings.DEFAULT_LOG_FORMAT)

        self.do_asf_activation()
        self.do_asf_initengine()
        self.do_asf_print_help()

    def do_asf_print_help(self):
        asf_version = self.do_asf_getversion()
        print '*' * 80
        print '{0} Author: {1}'.format(self.__class__.__name__, 'forcemain@163.com')
        print '''Library Dependence:
        libarcsoft_face.so
        libarcsoft_face_engine.so
            Version: {0}
            BuildDate: {1}
            CopyRight: {2}
        '''.format(asf_version.contents.Version, asf_version.contents.BuildDate, asf_version.contents.CopyRight)
        print '*' * 80

    def do_asf_getversion(self):
        from arcsoft.util.asf_getversion import func_asf_getversion

        ret = func_asf_getversion(self.handle)
        if ret:
            logger.debug('Do asf getversion success, ret={0}'.format(ret))
        else:
            logger.error('Do asf getversion success, ret=null')

        return ret

    def do_asf_activation(self):
        from arcsoft.util.asf_activation import func_asf_activation

        ret_succ = {0: 'activation', 90114: 'already activation'}
        ret = func_asf_activation(self.app_id, self.sdk_key)
        ret_isok = ret in ret_succ
        if ret_isok:
            logger.debug('Do asf activation success, {0}'.format(ret_succ[ret]))
        else:
            logger.error('Do asf activation failure, ret={0}'.format(ret))

        return ret_isok

    def do_asf_initengine(self, mode=0xFFFFFFFF, orient=0x1, scale_val=16, max_num=50, mask=5):
        from arcsoft.util.asf_initengine import func_asf_initengine

        ret = func_asf_initengine(mode, orient, scale_val, max_num, mask, byref(self.handle))
        if ret == 0:
            logger.debug('Do asf initengine success, ret=0')
        else:
            logger.error('Do asf initengine failure, ret={0}'.format(ret))

        return ret, self.handle

    def do_asf_detectfaces(self, path):
        from arcsoft.core.structure import ASFMultipleFaceInfo
        from arcsoft.util.asf_detectfaces import detectfaces_from_file
        from arcsoft.util.asvl_color_format import ASVL_PAF_RGB24_B8G8R8

        faces = ASFMultipleFaceInfo()
        ret = detectfaces_from_file(path, handle=self.handle, format=ASVL_PAF_RGB24_B8G8R8, faces=byref(faces))
        if ret == 0:
            logger.debug('Do asf detectfaces success, faceNum={0}'.format(faces.faceNum))
            face_image_name, dot, face_image_ext = os.path.basename(path).rpartition('.')
            if self.debug:
                for i in xrange(faces.faceNum):
                    cur_rect, cur_orient = faces.faceRect[i], faces.faceOrient[i]
                    face_image = cv2.imread(path)
                    crop_image = face_image[cur_rect.top: cur_rect.bottom, cur_rect.left: cur_rect.right]
                    face_image = Image.fromarray(crop_image)
                    cv2.imwrite('{0}_face{1}_corp{2}{3}'.format(face_image_name, i+1, dot, face_image_ext),
                                numpy.array(face_image))
                    msg = '#{0} face, faceRect({1}, {2}, {3}, {4}) faceOrient({5})'.format(i+1, cur_rect.left,
                                                                                           cur_rect.top, cur_rect.right,
                                                                                           cur_rect.bottom, cur_orient)
                    logger.debug(msg)
        else:
            logger.error('Do asf detectfaces failure, ret={0}'.format(ret))

        return ret, faces

    def do_face_recognition(self):
        pass
