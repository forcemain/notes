#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import sys


reload(sys)
sys.setdefaultencoding('utf-8')


MOK = 0
MERR_UNKNOWN = 1


FFDFFR_EXCEPTIONS = {
    MOK: ('MOK', u'成功'),
    MERR_UNKNOWN: ('MERR_UNKNOWN', u'错误原因不明'),
}


class FFDFFRException(Exception):
    def __init__(self, code=1, name=FFDFFR_EXCEPTIONS[1][0], mesg=FFDFFR_EXCEPTIONS[1][1]):
        super(FFDFFRException, self).__init__()
        self.code = code
        self.name = name
        self.mesg = mesg

    def __str__(self):
        return '<{0}: code={1} name={2} mesg={3}>'.format(self.__class__.__name__, self.code, self.name, self.mesg)
