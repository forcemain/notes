#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import io


from ctypes import *
from PIL import Image
from arcsoft.util.logger import Logger
from arcsoft.util.loader.engine_loader import engine
from arcsoft.core.structure import ASFMultipleFaceInfo


logger = Logger.get_logger(__file__)


func_asf_detectfaces = engine.ASFDetectFaces
func_asf_detectfaces.restype = c_int32
func_asf_detectfaces.argtypes = (c_void_p, c_int32, c_int32, c_int32, POINTER(c_int8), POINTER(ASFMultipleFaceInfo))


def get_bgr_from_image(path):
    old_image = Image.open(path)
    width = old_image.width & 0xFFFFFFFC
    height = old_image.height & 0xFFFFFFFE
    if width != old_image.width or height != old_image.height:
        new_image = old_image.crop((0, 0, width, height))
    else:
        new_image = old_image
    new_image_bytes = io.BytesIO()
    new_image.transpose(Image.FLIP_TOP_BOTTOM).convert('RGB').save(new_image_bytes, format='BMP')

    return bytes(new_image_bytes.getvalue()[54:]), width, height


def detectfaces_from_video(path, **kwargs):
    pass


def detectfaces_from_image(path, **kwargs):
    handle, format, faces = map(lambda k: kwargs.get(k), ('handle', 'format', 'faces'))
    new_image, width, height = get_bgr_from_image(path)
    imagedata = cast(new_image, POINTER(c_byte))

    return func_asf_detectfaces(handle, width, height, format, imagedata, faces)


def detectfaces_from_file(path, **kwargs):
    media_type = kwargs.pop('media_type', 'image')

    assert media_type in ('image', 'video'), 'Not yet supported {0}'.format(media_type)

    return detectfaces_from_image(path, **kwargs) if media_type == 'image' else detectfaces_from_video(path, **kwargs)
