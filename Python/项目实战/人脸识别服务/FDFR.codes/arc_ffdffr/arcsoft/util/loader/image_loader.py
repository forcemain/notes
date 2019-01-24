#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import cv2


from functools import partial
from arcsoft.core.structure import A


def image_load(path):
    # f_img = FaceImage(path)
    image = cv2.imread(face_image.path)
    image_shape = image.shape
    image = cv2.resize(image, (image_shape[1]//4*4, image_shape[0]//4*4))
    image_shape = image.shape
    f_img.data = image
    f_img.height, f_img.width = image_shape[0], image_shape[1]

    return f_img


image = partial(image_load)
