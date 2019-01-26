# ! -*- coding: utf-8 -*-


# author: forcemain@163.com


from requests import request


from ..utils.logger import Logger
from .exceptions import SdkException
from .request.base import BaseRequest


logger = Logger.get_logger(__file__)


class Client(object):
    FFD_ENDPOINT = ''

    def __init__(self, **kwargs):
        self._endpoint = kwargs.get('endpoint', self.FFD_ENDPOINT)

    def sign(self):
        # Not yet provided
        pass

    def get_url(self, ffd_request):
        return '{0}/{1}'.format(self._endpoint.rstrip('/'), ffd_request.get_uri().lstrip('/'))

    def send(self, ffd_request, **kwargs):
        assert isinstance(ffd_request, BaseRequest), 'ffd_request must be instanceof BaseRequest'
        method, url = ffd_request.get_method(), self.get_url(ffd_request)
        logger.debug('{0} {1} {2}'.format(method.capitalize(), url, ffd_request))
        kwargs.update(ffd_request.to_req_kwargs())

        response = request(method, url, **kwargs).json()
        if response['status'] != '000000':
            raise SdkException(code=response['status'], message=response['detail'])

        return response
