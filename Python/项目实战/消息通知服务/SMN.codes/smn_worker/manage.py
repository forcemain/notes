#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import sys
import fire
import unittest


from worker import settings
from worker.data import get_worker_dir


reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.insert(0, get_worker_dir())


class SMSWorker(object):
    def __init__(self, **kwargs):
        from worker.core.manager import SMSManager

        kwargs['pub_channel'] = kwargs.get('pub_channel', settings.RDS_SMN_SMS_PUB_CHANNEL)
        kwargs['sub_channel'] = kwargs.get('sub_channel', settings.RDS_SMN_SMS_SUB_CHANNEL)
        self.worker = SMSManager(**kwargs)

    def start(self):
        self.worker.listen()


class HTTPWorker(object):
    def __init__(self, **kwargs):
        from worker.core.manager import HTTPManager

        kwargs['pub_channel'] = kwargs.get('pub_channel', settings.RDS_SMN_HTTP_PUB_CHANNEL)
        kwargs['sub_channel'] = kwargs.get('sub_channel', settings.RDS_SMN_HTTP_SUB_CHANNEL)
        self.worker = HTTPManager(**kwargs)

    def start(self):
        self.worker.listen()


class HTTPSWorker(object):
    def __init__(self, **kwargs):
        from worker.core.manager import HTTPSManager

        kwargs['pub_channel'] = kwargs.get('pub_channel', settings.RDS_SMN_HTTPS_PUB_CHANNEL)
        kwargs['sub_channel'] = kwargs.get('sub_channel', settings.RDS_SMN_HTTPS_SUB_CHANNEL)
        self.worker = HTTPSManager(**kwargs)

    def start(self):
        self.worker.listen()


class EmailWorker(object):
    """
    Email worker event:
    {
        'subject': 'email subject',
        'alias_name': 'email sender alias name',
        'eventutctime': 0,
        'time_to_live': 3600,
        'message': {
            'to': [],
            'cc': [],
            'contents': 'support html, even embedded some pictures or attachments',
            'payloads': [{
                'data': 'base64 data'
                'name': 'file name, when embedded pictures or attachments useful',
                'type': "support text and image, corresponding attachments and pictures"
            }]
        }
    }
    """
    def __init__(self, **kwargs):
        from worker.core.manager import EmailManager

        kwargs['pub_channel'] = kwargs.get('pub_channel', settings.RDS_SMN_EMAIL_PUB_CHANNEL)
        kwargs['sub_channel'] = kwargs.get('sub_channel', settings.RDS_SMN_EMAIL_SUB_CHANNEL)
        self.worker = EmailManager(**kwargs)

    def start(self):
        self.worker.listen()


class WorkerManager(object):
    def __init__(self, **kwargs):
        self.run_as_sms = SMSWorker(**kwargs)
        self.run_as_http = HTTPSWorker(**kwargs)
        self.run_as_https = HTTPSWorker(**kwargs)
        self.run_as_email = EmailWorker(**kwargs)

    @staticmethod
    def run_sms_unittests():
        pass

    @staticmethod
    def run_http_unittests():
        pass

    @staticmethod
    def run_https_unittests():
        pass

    @staticmethod
    def run_email_unittests():
        from worker.tests.test_smn_email import SmnEmailTestCase

        suite = unittest.TestSuite()
        suite.addTests(SmnEmailTestCase.to_tests())

        runner = unittest.TextTestRunner()
        runner.run(suite)


if __name__ == '__main__':
    fire.Fire(WorkerManager)


