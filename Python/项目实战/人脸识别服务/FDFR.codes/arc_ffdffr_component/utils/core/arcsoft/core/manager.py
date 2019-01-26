#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import logging


from ctypes import *
from arcsoft.core import exception
from arcsoft.data import SdkLoader
from arcsoft.utils.logger import Logger
from arcsoft import settings, get_authors, get_version
from arcsoft.core.decorator import exit_with_exception


logger = Logger.get_logger(__file__)


class BaseManager(object):
    depent = None
    fd_handle = c_void_p()
    fr_handle = c_void_p()
    ft_handle = c_void_p()
    ua_handle = c_void_p()
    ug_handle = c_void_p()

    def __init__(self, **kwargs):
        self.dustbin = set()
        self.library = CDLL(self.depent)
        self.debug = kwargs.get('debug', True)
        self.app_id = kwargs.get('app_id', settings.APP_ID)
        self.fd_key = kwargs.get('fd_key', settings.FD_KEY)
        self.ft_key = kwargs.get('ft_key', settings.FT_KEY)
        self.fr_key = kwargs.get('fr_key', settings.FR_KEY)
        self.ua_key = kwargs.get('ua_key', settings.UA_KEY)
        self.ug_key = kwargs.get('ug_key', settings.UG_KEY)

    def do_setup(self):
        if not self.debug:
            return
        logging.basicConfig(level=settings.DEFAULT_LOG_LEVEL, format=settings.DEFAULT_LOG_FORMAT)

        self.do_initial_engine()
        self.do_print_info()

    def do_initial_engine(self, **kwargs):
        raise NotImplementedError

    def do_print_info(self):
        version = self.do_get_version()
        print '*' * 100
        print '*{0} Authors: {1}'.format(self.__class__.__name__, get_authors())
        print '''*Library Dependence (ArcFace C++ SDK V{0}):
        {1}
        BuildDate: {2}
        Version: {3}
        CopyRight: {4}
        '''.format(get_version(), self.depent, version.contents.BuildDate, version.contents.Version,
                   version.contents.CopyRight)
        print '*' * 100

    def do_get_version(self):
        raise NotImplementedError

    def do_uninitial_engine(self):
        raise NotImplementedError

    def __enter__(self):
        self.do_setup()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.do_uninitial_engine()


class AgeEstimationManager(BaseManager):
    depent = SdkLoader().age_estimation_path

    def __init__(self, **kwargs):
        super(AgeEstimationManager, self).__init__(**kwargs)

    def do_print_info(self):
        pass

    def do_initial_engine(self):
        pass

    def do_get_version(self):
        pass

    def do_uninitial_engine(self):
        pass


class FaceDetectionManager(BaseManager):
    depent = SdkLoader().face_detection_path

    def __init__(self, **kwargs):
        super(FaceDetectionManager, self).__init__(**kwargs)

    @exit_with_exception
    def do_initial_engine(self, **kwargs):
        from arcsoft.pysdk.loader.libc_loader import libc
        from arcsoft.const.fd import AFD_FSDK_ORIENT_PRIORITY
        from arcsoft.pysdk.fd.afd_initial_engine import func_initial_engine

        p_mem = kwargs.get('p_mem', libc.malloc(c_size_t(settings.FD_WORK_BUFFER_SIZE)))
        self.dustbin.add(p_mem)
        i_mem_size = kwargs.get('i_mem_size', c_int32(settings.FD_WORK_BUFFER_SIZE))
        p_engine = kwargs.get('p_engine', byref(self.fd_handle))
        i_orient_priority = kwargs.get('i_orient_priority', AFD_FSDK_ORIENT_PRIORITY.AFD_FSDK_OPF_0_HIGHER_EXT)
        n_scale = kwargs.get('n_scale', 16)
        n_max_face_num = kwargs.get('n_max_face_num', 50)
        ret = func_initial_engine(self.library)(self.app_id, self.fd_key, p_mem, i_mem_size, p_engine,
                                                i_orient_priority, n_scale, n_max_face_num)
        if ret == exception.MOK:
            logger.debug('{0} do_initial_engine success'.format(self.__class__.__name__))
        else:
            logger.error('{0} do_initial_engine failure, ret={1}'.format(self.__class__.__name__, ret))

        return ret,

    def do_get_version(self):
        from arcsoft.pysdk.fd.afd_get_version import func_get_version

        return func_get_version(self.library)(self.fd_handle)

    @exit_with_exception
    def do_uninitial_engine(self):
        from arcsoft.pysdk.loader.libc_loader import libc
        from arcsoft.pysdk.fd.afd_uninitial_engine import func_uninitial_engine

        ret = func_uninitial_engine(self.library)(self.fd_handle)
        while self.dustbin:
            libc.free(self.dustbin.pop())
        if ret == exception.MOK:
            logger.debug('{0} do_uninitial_engine success'.format(self.__class__.__name__))
        else:
            logger.error('{0} do_uninitial_engine failure, ret={1}'.format(self.__class__.__name__, ret))

        return ret,

    @exit_with_exception
    def do_still_image_detection(self, path, **kwargs):
        from arcsoft.model import SingleFace
        from arcsoft.model.fd import AfdFsdkFaceres
        from arcsoft.pysdk.loader.image_loader import BGRImage, gen_bgr_from_image
        from arcsoft.pysdk.fd.afd_still_image_detection import func_still_image_detection

        multi_faces = []
        image = BGRImage(path=path)
        faces = POINTER(AfdFsdkFaceres)()
        gen_bgr_from_image(image)

        ret = func_still_image_detection(self.library)(self.fd_handle, image.to_asvl_offscreen(**kwargs), faces)
        n_face = faces.contents.nFace
        rcface = faces.contents.rcFace
        o_face = faces.contents.lfaceOrient
        if ret == exception.MOK:
            logger.debug('{0} do_still_image_detection success, path={1} nFace={2}'.format(self.__class__.__name__,
                                                                                           path, n_face))
            if self.debug:
                for i in xrange(n_face):
                    c_rect = rcface[i]
                    c_orient = o_face[i]
                    logger.debug('{0} found #{1} rcFace=(left: {2} top: {3} right: {4} bottom: {5}) Orient={6}'.format(
                        self.__class__.__name__, i + 1, c_rect.left, c_rect.top, c_rect.right, c_rect.bottom, c_orient
                    ))
        else:
            logger.error('{0} do_uninitial_engine failure, ret={1}'.format(self.__class__.__name__, ret))

        for i in xrange(n_face):
            c_rect = rcface[i]
            c_orient = o_face[i]
            c_face = SingleFace(left=c_rect.left, top=c_rect.top, right=c_rect.right, bottom=c_rect.bottom,
                                image=image, orient=c_orient)
            multi_faces.append(c_face)

        return ret, multi_faces


class FaceRecognitionManager(BaseManager):
    depent = SdkLoader().face_recognition_path

    def __init__(self, **kwargs):
        super(FaceRecognitionManager, self).__init__(**kwargs)

    def do_print_info(self):
        version = self.do_get_version()
        print '*' * 100
        print '*{0} Authors: {1}'.format(self.__class__.__name__, get_authors())
        print '''*Library Dependence (ArcFace C++ SDK V{0}):
        {1}
        BuildDate: {2}
        Version: {3}
        CopyRight: {4}
        lFeatureLevel: {5}
        '''.format(get_version(), self.depent, version.contents.BuildDate, version.contents.Version,
                   version.contents.CopyRight, version.contents.lFeatureLevel)
        print '*' * 100

    @exit_with_exception
    def do_initial_engine(self, **kwargs):
        from arcsoft.pysdk.loader.libc_loader import libc
        from arcsoft.pysdk.fr.afr_initial_engine import func_initial_engine

        p_mem = kwargs.get('p_mem', libc.malloc(c_size_t(settings.FR_WORK_BUFFER_SIZE)))
        self.dustbin.add(p_mem)
        i_mem_size = kwargs.get('i_mem_size', c_int32(settings.FR_WORK_BUFFER_SIZE))
        p_engine = kwargs.get('p_engine', byref(self.fr_handle))
        ret = func_initial_engine(self.library)(self.app_id, self.fr_key, p_mem, i_mem_size, p_engine)
        if ret == exception.MOK:
            logger.debug('{0} do_initial_engine success'.format(self.__class__.__name__))
        else:
            logger.error('{0} do_initial_engine failure, ret={1}'.format(self.__class__.__name__, ret))

        return ret,

    def do_get_version(self):
        from arcsoft.pysdk.fr.afr_get_version import func_get_version

        return func_get_version(self.library)(self.fr_handle)

    @exit_with_exception
    def do_uninitial_engine(self):
        from arcsoft.pysdk.loader.libc_loader import libc
        from arcsoft.pysdk.fr.afr_uninitial_engine import func_uninitial_engine

        ret = func_uninitial_engine(self.library)(self.fr_handle)
        while self.dustbin:
            libc.free(self.dustbin.pop())
        if ret == exception.MOK:
            logger.debug('{0} do_uninitial_engine success'.format(self.__class__.__name__))
        else:
            logger.error('{0} do_uninitial_engine failure, ret={1}'.format(self.__class__.__name__, ret))

        return ret,

    @exit_with_exception
    def do_extract_frfeature(self, face, **kwargs):
        from arcsoft.model.fr import AfrFsdkFaceInput, AfrFsdkFaceModel
        from arcsoft.pysdk.fr.afr_extract_frfeature import func_extract_frfeature

        face_input = AfrFsdkFaceInput()
        face_feature = AfrFsdkFaceModel()

        face_input.lOrient = face.orient
        face_input.rcFace.left = face.left
        face_input.rcFace.top = face.top
        face_input.rcFace.right = face.right
        face_input.rcFace.bottom = face.bottom

        ret = func_extract_frfeature(self.library)(self.fr_handle, face.image.to_asvl_offscreen(**kwargs), face_input,
                                                   face_feature)
        if ret == exception.MOK:
            future_point = len(face_feature.to_bytearray())
            logger.debug('{0} do_extract_single_frfeature success, futurePoint={1}'.format(self.__class__.__name__,
                                                                                           future_point))
        else:
            logger.error('{0} do_extract_single_frfeature failure, ret={1}'.format(self.__class__.__name__, ret))

        return ret, face_feature.deepcopy()

    @exit_with_exception
    def do_facepair_matching(self, ref_feature, pro_befeature):
        from arcsoft.pysdk.fr.arf_facepair_matching import func_facepair_matching

        simil_score = c_float(0.0)
        ret = func_facepair_matching(self.library)(self.fr_handle, ref_feature, pro_befeature, simil_score)
        if ret == exception.MOK:
            logger.debug('{0} do_facepair_matching success, fSimilScore={1}'.format(self.__class__.__name__,
                                                                                    simil_score))
        else:
            logger.error('{0} do_facepair_matching failure, ret={1}'.format(self.__class__.__name__, ret))

        return ret, simil_score


class FaceTrackingManager(BaseManager):
    depent = SdkLoader().face_tracking_path

    def __init__(self, **kwargs):
        super(FaceTrackingManager, self).__init__(**kwargs)

    def do_initial_engine(self):
        pass

    def do_get_version(self):
        pass

    def do_uninitial_engine(self):
        pass


class GenderEstimationManager(BaseManager):
    depent = SdkLoader.gender_estimation_path

    def __init__(self, **kwargs):
        super(GenderEstimationManager, self).__init__(**kwargs)

    def do_initial_engine(self):
        pass

    def do_get_version(self):
        pass

    def do_uninitial_engine(self):
        pass
