#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import json
import time


from worker import settings
from worker.tests import SmnTestCase


class SmnEmailTestCase(SmnTestCase):
    """
    Smn email event model:
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

    def test_smn_plain_email(self):
        msg = json.dumps({
            'subject': '{0}_{1}'.format(self.__class__.__name__, u'测试明文邮件,请忽略!'),
            'alias_name': u'SMN系统代发', 'eventutctime': time.time(), 'time_to_live': 3600,
            'message': {
                'to': [settings.SMN_EMAIL_SMTP_USER],
                'contents': '{0} With {1}'.format(u'本次测试(成功)', self.__class__.__name__)
            }
        })
        res = self.rds_helper.publish(msg)

        self.assertTrue(res, True)

    def test_smn_html_email(self):
        msg = json.dumps({
            'subject': '{0}_{1}'.format(self.__class__.__name__, u'测试网页邮件,请忽略!'),
            'alias_name': u'SMN系统代发', 'eventutctime': time.time(), 'time_to_live': 3600,
            'message': {
                'to': [settings.SMN_EMAIL_SMTP_USER],
                'contents': '{0} With {1}'.format(u'本次测试(<font color="green">成功</font>)', self.__class__.__name__)
            }
        })
        res = self.rds_helper.publish(msg)

        self.assertTrue(res, True)

    def test_smn_image_email(self):
        fly = (
            'R0lGODdhoAB4AOfXAAAAADMAAGYAAJkAAMwAAP8AAAAzADMzAGYzAJkzAMwzAP8zAABmADNmAGZmAJlmAMxmAP9mAACZADOZAGaZAJmZAM'
            'yZAP+ZAADMADPMAGbMAJnMAMzMAP/MAAD/ADP/AGb/AJn/AMz/AP//AAAAMzMAM2YAM5kAM8wAM/8AMwAzMzMzM2YzM5kzM8wzM/8zMwBm'
            'MzNmM2ZmM5lmM8xmM/9mMwCZMzOZM2aZM5mZM8yZM/+ZMwDMMzPMM2bMM5nMM8zMM//MMwD/MzP/M2b/M5n/M8z/M///MwAAZjMAZmYAZp'
            'kAZswAZv8AZgAzZjMzZmYzZpkzZswzZv8zZgBmZjNmZmZmZplmZsxmZv9mZgCZZjOZZmaZZpmZZsyZZv+ZZgDMZjPMZmbMZpnMZszMZv/M'
            'ZgD/ZjP/Zmb/Zpn/Zsz/Zv//ZgAAmTMAmWYAmZkAmcwAmf8AmQAzmTMzmWYzmZkzmcwzmf8zmQBmmTNmmWZmmZlmmcxmmf9mmQCZmTOZmW'
            'aZmZmZmcyZmf+ZmQDMmTPMmWbMmZnMmczMmf/MmQD/mTP/mWb/mZn/mcz/mf//mQAAzDMAzGYAzJkAzMwAzP8AzAAzzDMzzGYzzJkzzMwz'
            'zP8zzABmzDNmzGZmzJlmzMxmzP9mzACZzDOZzGaZzJmZzMyZzP+ZzADMzDPMzGbMzJnMzMzMzP/MzAD/zDP/zGb/zJn/zMz/zP//zAAA/z'
            'MA/2YA/5kA/8wA//8A/wAz/zMz/2Yz/5kz/8wz//8z/wBm/zNm/2Zm/5lm/8xm//9m/wCZ/zOZ/2aZ/5mZ/8yZ//+Z/wDM/zPM/2bM/5nM'
            '/8zM///M/wD//zP//2b//5n//8z//////////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
            'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH/C05FVFNDQVBFMi4w'
            'AwEAAAAh+QQFCADYACwAAAAAoAB4AAAI/gCvCRxIsKDBgwgTKlzIsKHDhxAjSpxIsaLFixgzatzIsaPHjyBDihxJsqTJkyhTqlzJsqXLlz'
            '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'
            'c/i75pc7Tp06hTq84ZEAA7DQoADQoA'
        )
        msg = json.dumps({
            'subject': '{0}_{1}'.format(self.__class__.__name__, u'测试图片邮件,请忽略!'),
            'alias_name': u'SMN系统代发', 'eventutctime': time.time(), 'time_to_live': 3600,
            'message': {
                'to': [settings.SMN_EMAIL_SMTP_USER],
                'contents': '{0} With {1}<img src="cid:fly">'.format(u'本次测试(成功)', self.__class__.__name__),
                'payloads': [{
                    'data': fly,
                    'name': 'fly.gif',
                    'type': 'image'
                }]
            }
        })
        res = self.rds_helper.publish(msg)

        self.assertTrue(res, True)

    def test_smn_attachment_email(self):
        log = (
            'MjAxOS0wMi0xNSAyMDozNzoxNSwwMjEgLSB3b3JrZXIuY29yZS5tYW5hZ2VyIC0gL1VzZXJzL21hbm1hbmxpL0dpdGh1Yi9zbW5fd29ya2'
            'VyL3dvcmtlci9jb3JlL21hbmFnZXIucHkgLSA4NiAtIERFQlVHIC0gQ29ubmVjdCB0byByZWRpczovLzpmb3JjZW1haW5AMTI3LjAuMC4x'
            'OjYzNzkvMSBzdWNj'
        )
        msg = json.dumps({
            'subject': '{0}_{1}'.format(self.__class__.__name__, u'测试附件邮件,请忽略!'),
            'alias_name': u'SMN系统代发', 'eventutctime': time.time(), 'time_to_live': 3600,
            'message': {
                'to': [settings.SMN_EMAIL_SMTP_USER],
                'contents': '{0} With {1}'.format(u'本次测试(成功)', self.__class__.__name__),
                'payloads': [{
                    'data': log,
                    'name': 'smn_worker.log',
                    'type': 'text'
                }]
            }
        })
        res = self.rds_helper.publish(msg)

        self.assertTrue(res, True)
