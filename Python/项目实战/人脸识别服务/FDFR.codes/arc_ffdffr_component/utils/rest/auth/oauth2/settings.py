#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf import settings
from rest_framework.settings import APISettings


USER_SETTINGS = getattr(settings, 'OAUTH2_CLIENT', {})


DEFAULTS = {
    'OAUTH2_CLIENT_TOKEN_MODEL': None,
    'OAUTH2_SERVER_USER_ENDPOINT': None,
    'OAUTH2_SERVER_BEARER_HEADER_PREFIX': 'Bearer',
    'OAUTH2_CLIENT_TOKEN_MODEL_NAME': 'OAuth2Token',
    'OAUTH2_SERVER_TOKEN_EXPIRED_SECONDS': 24 * 60 * 60
}


IMPORT_STRINGS = (

)


oauth2_client_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
