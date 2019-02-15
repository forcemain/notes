#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import json
import time
import base64


from worker.core import exceptions
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class BaseModel(object):
    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)

        self._validators = set()

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        map(lambda k: setattr(instance, k, data[k]), data)

        return instance

    @classmethod
    def from_json(cls, data):
        dict_data = json.loads(data)

        return cls.from_dict(dict_data)

    def clean(self):
        map(lambda validator: validator(), self._validators)

    def to_dict(self):
        raise NotImplementedError

    def to_json(self, indent=4):
        dict_data = self.to_dict()

        return json.dumps(dict_data, indent=indent)

    def __str__(self):
        return '<{0}:{1}>'.format(self.__class__.__name__, self.to_json())


class BaseEventModel(BaseModel):
    def __init__(self, **kwargs):
        super(BaseEventModel, self).__init__(**kwargs)

        self.subject = kwargs.get('subject', None)
        self.message = kwargs.get('message', None)
        self.alias_name = kwargs.get('alias_name', '')
        self.eventutctime = kwargs.get('eventutctime', None)
        self.time_to_live = kwargs.get('time_to_live', 3600)

        map(lambda v: self._validators.add(v), [
            self.validate_subject,
            self.validate_message,
            self.valiudate_alias_name,
            self.validate_eventutctime,
            self.validate_time_to_live,
        ])

    def was_expired(self):
        return time.time() - self.eventutctime > self.time_to_live

    def validate_subject(self):
        if self.subject:
            return
        raise exceptions.InvalidEmailEventSubject

    def validate_message(self):
        if self.message:
            return
        raise exceptions.InvalidEmailEventMessage

    def valiudate_alias_name(self):
        return

    def validate_eventutctime(self):
        if self.eventutctime and isinstance(self.eventutctime, (float, int)):
            return
        raise exceptions.InvalidEmailEventUTCTime

    def validate_time_to_live(self):
        if self.time_to_live and isinstance(self.time_to_live, (float, int)):
            return
        raise exceptions.InvalidEmailEventTimeToLive

    def to_dict(self):
        pass

    def get_subject(self):
        return self.subject

    def set_subject(self, subject):
        self.subject = subject

    def get_message(self):
        return self.message

    def set_message(self, message):
        self.message = message

    def get_alias_name(self):
        return self.alias_name

    def set_alias_name(self, alias_name):
        self.alias_name = alias_name

    def get_eventutctime(self):
        return self.eventutctime

    def set_eventutctime(self, eventutctime):
        self.eventutctime = eventutctime

    def get_time_to_live(self):
        return self.time_to_live

    def set_time_to_live(self, time_to_live):
        self.time_to_live = time_to_live


class SMSMessageModel(BaseModel):
    def __init__(self, **kwargs):
        super(SMSMessageModel, self).__init__(**kwargs)

    def to_dict(self):
        pass


class SMSEventModel(BaseEventModel):
    def __init__(self, **kwargs):
        super(SMSEventModel, self).__init__(**kwargs)

    def to_dict(self):
        pass


class HTTPMessageModel(BaseModel):
    def __init__(self, **kwargs):
        super(HTTPMessageModel, self).__init__(**kwargs)

    def to_dict(self):
        pass


class HTTPEventModel(BaseEventModel):
    def __init__(self, **kwargs):
        super(HTTPEventModel, self).__init__(**kwargs)

    def to_dict(self):
        pass


class HTTPSMessageModel(BaseModel):
    def __init__(self, **kwargs):
        super(HTTPSMessageModel, self).__init__(**kwargs)

    def to_dict(self):
        pass


class HTTPSEventModel(BaseEventModel):
    def __init__(self, **kwargs):
        super(HTTPSEventModel, self).__init__(**kwargs)

    def to_dict(self):
        pass


class EmailPayloadModel(BaseModel):
    """
    Email payload model:
    {
        'data': '',
        'name': '',
        'type': 'text',
    }
    """
    def __init__(self, **kwargs):
        super(EmailPayloadModel, self).__init__(**kwargs)

        self.data = kwargs.get('data', '')
        self.name = kwargs.get('name', '')
        self.type = kwargs.get('type', 'text')

        map(lambda v: self._validators.add(v), [
            self.validate_data,
            self.validate_name,
            self.validate_type,
        ])

    def validate_data(self):
        try:
            base64.b64decode(self.data)
        except TypeError:
            raise exceptions.InvalidEmailPayloadData

    def validate_name(self):
        if self.name.count('.') == 1:
            return
        raise exceptions.InvalidEmailPayloadName

    def validate_type(self):
        if self.type in ('text', 'image'):
            return
        raise exceptions.InvalidEmailPayloadType

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def to_dict(self):
        data = {
            'data': self.get_data(),
            'name': self.get_name(),
            'type': self.get_type(),
        }

        return data

    def as_email_payload(self):
        payload_name = self.name.split('.')[0]
        payload_data = base64.b64decode(self.data)
        if self.type == 'image':
            payload = MIMEImage(payload_data)
            payload.add_header('Content-ID', payload_name)

            return payload
        payload = MIMEText(payload_data, 'base64', 'utf-8')
        payload.add_header('Content-type', 'application/octet-stream')
        payload.add_header('Content-Disposition', 'attachment;filename="{0}"'.format(self.name))

        return payload


class EmailMessageModel(BaseModel):
    """
    Email message model:
    {
        'to': [],
        'cc': [],
        'contents': '',
        'payloads': []
    }
    """
    def __init__(self, **kwargs):
        super(EmailMessageModel, self).__init__(**kwargs)

        self.to = kwargs.get('to', [])
        self.cc = kwargs.get('cc', [])
        self.contents = kwargs.get('contents', '')
        self.payloads = kwargs.get('payloads', ())

        map(lambda v: self._validators.add(v), [
            self.validate_to,
            self.validate_cc,
            self.validate_contents,
            self.validate_payloads,
        ])

    def validate_to(self):
        if self.to and isinstance(self.to, (list, tuple)):
            return
        raise exceptions.InvalidEmailMessageTo

    def validate_cc(self):
        if not self.cc or isinstance(self.cc, (list, tuple)):
            return
        raise exceptions.InvalidEmailMessageCc

    def validate_contents(self):
        if self.contents:
            return
        raise exceptions.InvalidEmailMessageContents

    def validate_payloads(self):
        for payload in self.payloads:
            payload.clean()

    def get_to(self):
        return self.to

    def set_to(self, to):
        self.to = to

    def get_cc(self):
        return self.cc

    def set_cc(self, cc):
        self.cc = cc

    def get_contents(self):
        return self.contents

    def set_contents(self, contents):
        self.contents = contents

    def get_payloads(self):
        return self.payloads

    def set_payloads(self, payloads):
        self.payloads = payloads

    def to_dict(self):
        data = {
            'to': self.get_to(),
            'contents': self.get_contents(),
            'payloads': self.get_payloads()
        }

        return data


class EmailEventModel(BaseEventModel):
    def __init__(self, **kwargs):
        super(EmailEventModel, self).__init__(**kwargs)

    def to_dict(self):
        data = {
            'subject': self.get_subject(),
            'message': self.get_message().to_dict(),
            'eventutctime': self.get_eventutctime(),
            'time_to_live': self.get_time_to_live(),
        }

        return data
