#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from functools import wraps
from arcsoft import settings
from traceback import format_exc
from arcsoft.core.exception import FFDFFRException, FFDFFR_EXCEPTIONS


def exit_with_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
            if ret[0] == 0:
                return ret
            exc_info = FFDFFR_EXCEPTIONS.get(ret[0], FFDFFR_EXCEPTIONS[1])
            raise FFDFFRException(code=ret[0], name=exc_info[0], mesg=exc_info[1])
        except Exception as e:
            if isinstance(e, FFDFFRException):
                raise e
            else:
                raise FFDFFRException(code=-1, name='RUN_UNKNOWN',
                                      mesg=format_exc() if settings.TRACE_EXCEPTION else e.message)
    return wrapper
