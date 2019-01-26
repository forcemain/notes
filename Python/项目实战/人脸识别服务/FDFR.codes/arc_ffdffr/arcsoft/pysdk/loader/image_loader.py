#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import io


from ctypes import *
from PIL import Image


class BGRImage(object):
    def __init__(self, path, width=0, height=0, imgdata=None):
        self.path = path
        self.width = width
        self.height = height
        self.imgdata = imgdata

    def to_asvl_offscreen(self, **kwargs):
        from arcsoft.model import c_ubyte_p, FsdkASVLOFFSCREEN
        from arcsoft.const.fd import AFD_FSDK_ASVL_COLOR_FORMAT

        asvl_offscreen = FsdkASVLOFFSCREEN()
        asvl_offscreen.u32PixelArrayFormat = kwargs.get('u32PixelArrayFormat',
                                                        AFD_FSDK_ASVL_COLOR_FORMAT.ASVL_PAF_RGB24_B8G8R8)
        asvl_offscreen.i32Width = kwargs.get('i32Width', self.width)
        asvl_offscreen.i32Height = kwargs.get('i32Height', self.height)
        asvl_offscreen.pi32Pitch[0] = self.width * 3
        asvl_offscreen.ppu8Plane[0] = cast(self.imgdata, c_ubyte_p)
        asvl_offscreen.ppu8Plane[1] = cast(0, c_ubyte_p)
        asvl_offscreen.ppu8Plane[2] = cast(0, c_ubyte_p)
        asvl_offscreen.ppu8Plane[3] = cast(0, c_ubyte_p)

        return asvl_offscreen


def gen_bgr_from_image(image, corp=()):
    old_image = Image.open(image.path)
    width = old_image.width & 0xFFFFFFFC
    height = old_image.height & 0xFFFFFFFE
    if width != old_image.width or height != old_image.height:
        new_image = old_image.crop(corp or (0, 0, width, height))
    else:
        new_image = old_image
    new_image_bytes = io.BytesIO()
    new_image.transpose(Image.FLIP_TOP_BOTTOM).convert('RGB').save(new_image_bytes, format='BMP')

    image.width, image.height, image.imgdata = width, height,  bytes(new_image_bytes.getvalue()[54:])

