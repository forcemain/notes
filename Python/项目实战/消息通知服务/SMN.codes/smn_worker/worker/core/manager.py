#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import time
import redis
import logging
import itertools


from threading import Thread
from worker.core import exceptions
from worker import models, settings
from worker.utils.logger import Logger
from worker.utils.common import gen_strs_md5
from worker.utils.redis_helper import RedisHelper
from worker.utils.handlers.email_handler import EmailHandler


logger = Logger.get_logger(__name__)


class HeartbeatReportThread(Thread):
    def __init__(self, manager, rds_helper):
        super(HeartbeatReportThread, self).__init__()

        self.manager = manager
        self.rds_helper = rds_helper
        self.counter = itertools.count(2, 2)

    def run_forever(self):
        pass

    def run(self):
        pass


class HandleEventThread(Thread):
    def __init__(self, manager, rds_helper):
        super(HandleEventThread, self).__init__()

        self.manager = manager
        self.rds_helper = rds_helper
        self.counter = itertools.count(2, 2)

    def write_result(self, key, ttl, code, message):
        """
        {
            'code': '',
            'message': ''
        }
        """
        self.manager.conn.srem(self.manager.result_set, key)
        result_hash = '{0}::{1}'.format(self.manager.result_set, key)
        self.manager.conn.hmset(result_hash, {
            'code': code, 'message': message
        })
        self.manager.conn.expire(result_hash, ttl)

    def run_forever(self, pubsub):
        while True:
            ttl, code, message = 3600, '0', 'Success'
            _type, channel, data = pubsub.parse_response()
            if _type != 'message':
                logger.warning('Invalid message, type={0}, ignored'.format(_type))
                continue
            try:
                ttl = self.manager.handle(data).get_time_to_live()
            except Exception as e:
                code = getattr(e, 'code', '1')
                message = 'Unknown error' if code == '1' else getattr(e, 'message', 'Unknown error')
                logger.error('Handle email event data {0} with exception, exp={1}'.format(data, e))
            else:
                logger.debug('Handle email event data {0} succ'.format(data))
            finally:
                md5 = gen_strs_md5(data)
                self.write_result(md5, ttl, code, message)

    def run(self):
        while True:
            sleep_time = 1
            try:
                pubsub = self.rds_helper.subscribe()
                logger.debug('Connect to {0} succ'.format(self.manager.rds_url))
                self.run_forever(pubsub)
            except redis.connection.RedisError:
                sleep_time = self.counter.next()
                logger.error('Cannot connect to {0}, {1} trying again in {2:.2f} seconds'.format(self.manager.rds_url,
                                                                                                 self.name,
                                                                                                 sleep_time))
            finally:
                time.sleep(sleep_time)


class BaseManager(object):
    def __init__(self, **kwargs):
        self._conn = None
        self._result_set = None

        self.counter = itertools.count(2, 2)
        self._debug = kwargs.get('debug', False)
        self.rds_url = kwargs.get('rds_url', None)
        self.pub_channel = kwargs.get('pub_channel', None)
        self.sub_channel = kwargs.get('sub_channel', None)
        self.rds_client = kwargs.get('rds_client', redis.Redis)

        self._debug and logging.basicConfig(level=settings.DEFAULT_LOG_LEVEL, format=settings.DEFAULT_LOG_FORMAT)

    @property
    def conn(self):
        if isinstance(self._conn, self.rds_client):
            return self._conn
        self._conn = self.rds_client.from_url(self.rds_url)

        return self._conn

    @property
    def result_set(self):
        if self._result_set is not None:
            return self._result_set
        suffix = self.sub_channel.split('::')[-1]
        self._result_set = '{0}{1}'.format(settings.RDS_SMN_RESULT_PREFIX, suffix)

        return self._result_set

    def handle(self, data):
        raise NotImplementedError

    def listen(self):
        rds_helper = RedisHelper(conn=self.conn, pub_channel=self.pub_channel, sub_channel=self.sub_channel)
        heartbeat_report_thread = HeartbeatReportThread(self, rds_helper)
        heartbeat_report_thread.setDaemon(True)
        heartbeat_report_thread.start()
        handle_event_thread = HandleEventThread(self, rds_helper)
        handle_event_thread.setDaemon(True)
        handle_event_thread.start()

        map(lambda s: time.sleep(s), self.counter)


class SMSManager(BaseManager):
    def handle(self, data):
        pass


class HTTPManager(BaseManager):
    def handle(self, data):
        pass


class HTTPSManager(BaseManager):
    def handle(self, data):
        pass


class EmailManager(BaseManager):
    def handle(self, data):
        email_payloads = []
        email_event = models.EmailEventModel.from_json(data)
        email_message = models.EmailMessageModel.from_dict(email_event.get_message())
        for payload in email_message.get_payloads():
            email_payload = models.EmailPayloadModel.from_dict(payload)
            email_payloads.append(email_payload)
        email_message.set_payloads(email_payloads)
        email_event.set_message(email_message)

        if email_event.was_expired():
            raise exceptions.EmailEventExpired

        email_message.clean()
        email_event.clean()

        sender = EmailHandler(debug=self._debug)
        email_payloads = map(lambda p: p.as_email_payload(), email_payloads)
        sender.send(
            name=email_event.get_alias_name(), _to=email_message.get_to(), _cc=email_message.get_cc(),
            subject=email_event.get_subject(), content=email_message.get_contents(), payloads=email_payloads
        )

        return email_event
