#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from django.conf import settings
from rest_framework import status
from django.test import TestCase, Client
from itsdangerous import TimedSerializer
from django.core.urlresolvers import reverse_lazy


from .. import models


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.cas_consumer, created = models.CasConsumer.objects.get_or_create(name='cas_app')
        self.access_key = self.cas_consumer.access_key
        self.secret_key = self.cas_consumer.secret_key
        self.redirect_to = 'https://www.baidu.com/'

    def tearDown(self):
        pass

    def test_request_token_with_get_method(self):
        url = reverse_lazy('cas_app:cas-request-token')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(models.CasToken.objects.count(), 0)

    def test_request_token_with_post_method_and_no_access_key(self):
        url = reverse_lazy('cas_app:cas-request-token')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('No public key', response.content)
        self.assertEqual(models.CasToken.objects.count(), 0)

    def test_request_token_with_post_method_and_access_key_and_signdata_and_no_login(self):
        url = reverse_lazy('cas_app:cas-request-token')
        serializer = TimedSerializer(self.secret_key)
        data = serializer.dumps({'redirect_to': self.redirect_to})
        data_extra = {
            'HTTP_X_SERVICES_PUBLIC_KEY': self.access_key,
        }
        response = self.client.post(url, data, content_type='application/json', **data_extra)
        response_data = serializer.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.cas_consumer.cas_tokens.count(), 1)
        self.assertIn('request_token', response_data)

        request_token = response_data['request_token']

        url = reverse_lazy('cas_app:cas-user-authentication')
        response = self.client.get(url, data={
            'request_token': request_token,
        })

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        print response
