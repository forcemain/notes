#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import six


from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.serializers import Serializer


from .exps_handler import errors


class JsonResponse(Response):
    def __init__(self, data=None, code=errors.SUCCESS, message=None,
                 template_name=None, headers=None, exception=False, content_type=None):
        super(Response, self).__init__(None, status=HTTP_200_OK)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = {'code': code,
                     'message': message if message else errors.MESSAGES.get(code, errors.UNKNOWN_ERROR),
                     'data': data}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value
