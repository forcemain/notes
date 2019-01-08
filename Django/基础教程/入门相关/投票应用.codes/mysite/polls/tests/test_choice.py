#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from faker import Faker
from django.test import Client
from django.utils import timezone
from django.test.utils import TestCase


from .. import models


class ChoiceTestCase(TestCase):
    faker = Faker()

    def setUp(self):
        self.question = models.Question.objects.create(
            question_text=self.faker.text(max_nb_chars=200), pub_date=timezone.now()
        )
        self.client = Client(enforce_csrf_checks=True)

    def tearDown(self):
        self.question.delete()
        models.Choice.objects.all().delete()

    def create_choice(self, **kwargs):
        votes = kwargs.get('votes', 0)
        question = kwargs.get('question', self.question)
        choice_text = kwargs.get('choice_text', self.faker.text(max_nb_chars=200))

        return models.Choice.objects.create(question=question, choice_text=choice_text, votes=votes)

    def test_create_choice(self):
        choice = self.create_choice()

        self.assertIsInstance(choice, models.Choice)
        self.assertEqual(choice.__unicode__(), choice.choice_text)
