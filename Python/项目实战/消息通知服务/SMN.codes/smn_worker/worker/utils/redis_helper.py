#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import redis


class RedisHelper(object):
    def __init__(self, **kwargs):
        self._conn = kwargs.get('conn', None)
        self._sub_channel = kwargs.get('sub_channel', None)
        self._pub_channel = kwargs.get('pub_channel', None)

    def get_conn(self):
        return self._conn

    def set_conn(self, conn):
        self._conn = conn

    def get_sub_channel(self):
        return self._sub_channel

    def set_sub_channel(self, sub_channel):
        self._sub_channel = sub_channel

    def get_pub_channel(self):
        return self._pub_channel

    def set_pub_channel(self, pub_channel):
        self._pub_channel = pub_channel

    def publish(self, msg):
        assert isinstance(self._conn, redis.Redis), 'redis.Redis instance required, {0} provided'.format(self._conn)

        self._conn.publish(self._pub_channel, msg)

        return True

    def subscribe(self):
        assert isinstance(self._conn, redis.Redis), 'redis.Redis instance required, {0} provided'.format(self._conn)

        pubsub = self._conn.pubsub()
        pubsub.subscribe(self._sub_channel)
        pubsub.parse_response()

        return pubsub
