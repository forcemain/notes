#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import redis
import unittest


from worker import settings
from worker.utils.redis_helper import RedisHelper


class SmnTestCase(unittest.TestCase):
    rds_url = 'redis://:forcemain@127.0.0.1:6379/1'

    def setUp(self):
        self.conn = redis.Redis.from_url(self.rds_url)
        self.rds_helper = RedisHelper(
            conn=self.conn,
            pub_channel=settings.RDS_SMN_EMAIL_PUB_CHANNEL,
            sub_channel=settings.RDS_SMN_EMAIL_SUB_CHANNEL,
        )

    def tearDown(self):
        pass

    @classmethod
    def to_tests(cls):
        tests = []
        for attr in dir(cls):
            func = getattr(cls, attr)
            if not callable(func) or not attr.startswith('test_'):
                continue
            tests.append(cls(attr))
        return tests
