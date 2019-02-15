#! -*- coding: utf-8 -*-


# author: forcemain@163.com


class EmailEventException(Exception):
    code = '6000'
    message = 'Invalid email event'

    def __str__(self):
        return self.message


class EmailEventExpired(EmailEventException):
    code = '6001'
    message = 'Expired email event'


class InvalidEmailEventSubject(EmailEventException):
    code = '6010'
    message = 'Invalid email event subject'


class InvalidEmailEventMessage(EmailEventException):
    code = '6011'
    message = 'Invalid email event message'


class InvalidEmailEventUTCTime(EmailEventException):
    code = '6012'
    message = 'Invalid email event eventutctime'


class InvalidEmailEventTimeToLive(EmailEventException):
    code = '6013'
    message = 'Invalid email event time_to_live'


class InvalidEmailPayloadData(EmailEventException):
    code = '6014'
    message = 'Invalid email payload data'


class InvalidEmailPayloadName(EmailEventException):
    code = '6015'
    message = 'Invalid email payload name'


class InvalidEmailPayloadType(EmailEventException):
    code = '6016'
    message = 'Invalid email payload type'


class InvalidEmailMessageTo(EmailEventException):
    code = '6017'
    message = 'Invalid email message to'


class InvalidEmailMessageCc(EmailEventException):
    code = '6018'
    message = 'Invalid email message cc'


class InvalidEmailMessageContents(EmailEventException):
    code = '6019'
    message = 'Invalid email message contents'


class InvalidEmailMessagePayloads(EmailEventException):
    code = '6020'
    message = 'Invalid email message payloads'

