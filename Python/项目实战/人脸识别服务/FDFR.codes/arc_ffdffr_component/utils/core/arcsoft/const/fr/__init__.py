#! -*- coding: utf-8 -*-


# author: forcemain@163.com


AFR_FSDK_ORIENT_CODE = type('AfrFsdkOrientCode', (object,), {
    'AFR_FSDK_FOC_0': 0x1,
    'AFR_FSDK_FOC_90': 0x2,
    'AFR_FSDK_FOC_270': 0x3,
    'AFR_FSDK_FOC_180': 0x4,
    'AFR_FSDK_FOC_30': 0x5,
    'AFR_FSDK_FOC_60': 0x6,
    'AFR_FSDK_FOC_120': 0x7,
    'AFR_FSDK_FOC_150': 0x8,
    'AFR_FSDK_FOC_210': 0x9,
    'AFR_FSDK_FOC_240':  0xa,
    'AFR_FSDK_FOC_300': 0xb,
    'AFR_FSDK_FOC_330': 0xc,
})


AFR_FSDK_ASVL_COLOR_FORMAT = type('AfrFsdkAsvlColorFormat', (object,), {
    'ASVL_PAF_I420': 0x601,
    'ASVL_PAF_YUYV': 0x501,
    'ASVL_PAF_RGB24_B8G8R8': 0x201,
})
