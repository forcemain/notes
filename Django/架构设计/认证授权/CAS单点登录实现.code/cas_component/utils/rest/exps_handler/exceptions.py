#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _


class ExceedMaxIdentityNumberLimit(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('Exceed maximum identify number limit.')
    default_code = 'permission_denied'

