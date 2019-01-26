#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import logging


from rest_framework.status import HTTP_200_OK
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


from . import settings
from .helper import is_pretty


logger = logging.getLogger('django')


def drf_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if not response and settings.CATCH_ALL_EXCEPTIONS:
        logging.exception(exc)
        exc = APIException(exc)
        response = exception_handler(exc, context)
    if response is not None:
        response.status_code = HTTP_200_OK
        if is_pretty(response):
            return response
        error_message = response.data.pop('detail', '')
        error_code = settings.FRIENDLY_EXCEPTION_DICT.get(
            exc.__class__.__name__)
        response.data['code'] = error_code
        response.data['message'] = error_message

    return response
