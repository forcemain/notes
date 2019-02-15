#! -*- coding: utf-8 -*-


# author: forcemain@163.com


import logging

# Smtp Settings
SMN_EMAIL_SMTP_PORT = 465
SMN_EMAIL_SMTP_HOST = 'smtp.163.com'
SMN_EMAIL_SMTP_PASS = '............'
SMN_EMAIL_SMTP_USER = 'forcemain@163.com'

# Result Settings
RDS_SMN_RESULT_PREFIX = 'smn::result::'
RDS_SMN_SMS_RESULT_SET = '{0}sms'.format(RDS_SMN_RESULT_PREFIX)
RDS_SMN_HTTPS_RESULT_SET = '{0}https'.format(RDS_SMN_RESULT_PREFIX)
RDS_SMN_HTTP_RESULT_SET = '{0}http'.format(RDS_SMN_RESULT_PREFIX)
RDS_SMN_EMAIL_RESULT_SET = '{0}email'.format(RDS_SMN_RESULT_PREFIX)

# Channel Settings
RDS_SMN_CHANNEL_PREFIX = 'smn::channel::'
RDS_SMN_SMS_PUB_CHANNEL = '{0}sms'.format(RDS_SMN_CHANNEL_PREFIX)
RDS_SMN_SMS_SUB_CHANNEL = '{0}sms'.format(RDS_SMN_CHANNEL_PREFIX)
RDS_SMN_HTTPS_PUB_CHANNEL = '{0}https'.format(RDS_SMN_CHANNEL_PREFIX)
RDS_SMN_HTTPS_SUB_CHANNEL = '{0}https'.format(RDS_SMN_CHANNEL_PREFIX)
RDS_SMN_HTTP_PUB_CHANNEL = '{0}http'.format(RDS_SMN_CHANNEL_PREFIX)
RDS_SMN_HTTP_SUB_CHANNEL = '{0}http'.format(RDS_SMN_CHANNEL_PREFIX)
RDS_SMN_EMAIL_PUB_CHANNEL = '{0}email'.format(RDS_SMN_CHANNEL_PREFIX)
RDS_SMN_EMAIL_SUB_CHANNEL = '{0}email'.format(RDS_SMN_CHANNEL_PREFIX)

# Logging Settings
DEFAULT_LOG_LEVEL = logging.DEBUG
DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(pathname)s - %(lineno)d - %(levelname)s - %(message)s'
