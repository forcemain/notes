# ! -*- coding: utf-8 -*-


# author: forcemain@163.com


from ..utils.logger import Logger


logger = Logger.get_logger(__file__)


class Client(object):
    SMN_ENDPOINT = 'http://127.0.0.1:8000'

    def __init__(self, access_key_id, secret_access_key, endpoint=None):
        self._ak = access_key_id
        self._sk = secret_access_key
        self._endpoint = endpoint or self.SMN_ENDPOINT

    def sign(self):
        pass

    def send(self, smn_request):
        pass
