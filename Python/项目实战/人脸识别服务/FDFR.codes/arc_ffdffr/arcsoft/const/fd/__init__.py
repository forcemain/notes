#! -*- coding: utf-8 -*-


# author: forcemain@163.com


AFD_FSDK_ORIENT_CODE = type('AfdFsdkOrientCode', (object,), {
    'AFD_FSDK_FOC_0': 0x1,
    'AFD_FSDK_FOC_90': 0x2,
    'AFD_FSDK_FOC_270': 0x3,
    'AFD_FSDK_FOC_180': 0x4,
    'AFD_FSDK_FOC_30': 0x5,
    'AFD_FSDK_FOC_60': 0x6,
    'AFD_FSDK_FOC_120': 0x7,
    'AFD_FSDK_FOC_150': 0x8,
    'AFD_FSDK_FOC_210': 0x9,
    'AFD_FSDK_FOC_240':  0xa,
    'AFD_FSDK_FOC_300': 0xb,
    'AFD_FSDK_FOC_330': 0xc,
})


AFD_FSDK_ORIENT_PRIORITY = type('AfdFsdkOrientPriority', (object,), {
    'AFD_FSDK_OPF_0_ONLY': 0x1,
    'AFD_FSDK_OPF_90_ONLY': 0x2,
    'AFD_FSDK_OPF_270_ONLY': 0x3,
    'AFD_FSDK_OPF_180_ONLY': 0x4,
    'AFD_FSDK_OPF_0_HIGHER_EXT': 0x5,
})


AFD_FSDK_ASVL_COLOR_FORMAT = type('AfdFsdkAsvlColorFormat', (object,), {
    'ASVL_PAF_I420': 0x601,
    'ASVL_PAF_YUYV': 0x501,
    'ASVL_PAF_RGB24_B8G8R8': 0x201,
})
