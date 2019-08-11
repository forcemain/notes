#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.utils.translation import ugettext_lazy as _


SUCCESS = '0'
UNKNOWN_ERROR = '1'


MESSAGES = {
    SUCCESS: _('success.'),
    UNKNOWN_ERROR: _('unknown error.')
}
