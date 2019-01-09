#! -*- coding: utf-8 -*-


# author: forcemain@163.com


from faker import Faker
from django.test import Client
from django.utils import timezone
from django.test.utils import TestCase
from django.core.urlresolvers import reverse_lazy


from .. import models


class QuestionTestCase(TestCase):
    faker = Faker('zh_CN')

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def tearDown(self):
        models.Question.objects.all().delete()

    def create_question(self, **kwargs):
        question_text = kwargs.get('question_text', self.faker.text(max_nb_chars=200)),
        pub_date = kwargs.get('pub_date', timezone.now())

        return models.Question.objects.create(question_text=question_text, pub_date=pub_date)

    def test_create_question(self):
        question = self.create_question()

        self.assertTrue(isinstance(question, models.Question))
        self.assertEqual(question.__unicode__(), question.question_text)

    def test_was_published_recently_with_old_question(self):
        pub_date = timezone.now() - timezone.timedelta(days=30)
        question = self.create_question(pub_date=pub_date)

        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_future_question(self):
        pub_date = timezone.now() + timezone.timedelta(days=30)
        question = self.create_question(pub_date=pub_date)

        self.assertIs(question.was_published_recently(), False)

    def test_index_view_with_no_question(self):
        url = reverse_lazy('polls:tpl-poll-index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('No polls are valiable', response.content)
        questions_pk = list(response.context['questions'].values_list('pk', flat=True))
        self.assertEqual(questions_pk, [])

    def test_index_view_with_future_question(self):
        pub_date = timezone.now() + timezone.timedelta(days=30)
        self.create_question(pub_date=pub_date)
        url = reverse_lazy('polls:tpl-poll-index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn('No polls are valiable', response.content)
        questions_pk = list(response.context['questions'].values_list('pk', flat=True))
        # future should not display
        self.assertEqual(questions_pk, [])

    def test_index_view_with_old_question(self):
        pub_date = timezone.now() - timezone.timedelta(days=30)
        question = self.create_question(pub_date=pub_date)
        url = reverse_lazy('polls:tpl-poll-index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('No polls are valiable', response.content)
        questions_pk = list(response.context['questions'].values_list('pk', flat=True))
        self.assertEqual(questions_pk, [question.pk])

    def test_index_view_with_future_and_old_question(self):
        future_pub_date = timezone.now() + timezone.timedelta(days=30)
        self.create_question(pub_date=future_pub_date)
        old_pub_date = timezone.now() - timezone.timedelta(days=30)
        old_question = self.create_question(pub_date=old_pub_date)
        url = reverse_lazy('polls:tpl-poll-index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('No polls are valiable', response.content)
        questions_pk = list(response.context['questions'].values_list('pk', flat=True))
        self.assertEqual(questions_pk, [old_question.pk])

    def test_index_view_with_two_old_question(self):
        old_pub_date = timezone.now() - timezone.timedelta(days=30)
        old_questions = []
        old_questions.append(self.create_question(pub_date=old_pub_date))
        old_questions.append(self.create_question(pub_date=old_pub_date))
        url = reverse_lazy('polls:tpl-poll-index')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('No polls are valiable', response.content)
        questions_pk = list(response.context['questions'].values_list('pk', flat=True))
        self.assertEqual(questions_pk, map(lambda p: p.pk, old_questions))

    def test_detail_view_with_future_question(self):
        pub_date = timezone.now() + timezone.timedelta(days=30)
        question = self.create_question(pub_date=pub_date)
        url = reverse_lazy('polls:tpl-poll-detail', kwargs={'question_pk': question.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_old_question(self):
        pub_date = timezone.now() - timezone.timedelta(days=30)
        question = self.create_question(pub_date=pub_date)
        url = reverse_lazy('polls:tpl-poll-detail', kwargs={'question_pk': question.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        question_pk = response.context['question'].pk
        self.assertEqual(question_pk, question.pk)

    def test_result_view_with_future_question(self):
        pub_date = timezone.now() + timezone.timedelta(days=30)
        question = self.create_question(pub_date=pub_date)
        url = reverse_lazy('polls:tpl-poll-result', kwargs={'question_pk': question.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_result_view_with_old_question(self):
        pub_date = timezone.now() - timezone.timedelta(days=30)
        question = self.create_question(pub_date=pub_date)
        url = reverse_lazy('polls:tpl-poll-result', kwargs={'question_pk': question.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        question_pk = response.context['question'].pk
        self.assertEqual(question_pk, question.pk)

    def test_vote_view_with_future_question_and_selected_choice(self):
        pub_date = timezone.now() + timezone.timedelta(days=30)
        question = self.create_question(pub_date=pub_date)
        choice = question.choice_set.create(choice_text=self.faker.text(max_nb_chars=200))

        url = reverse_lazy('polls:rdr-poll-vote', kwargs={'question_pk': question.pk})
        response = self.client.post(url, {'choice_pk': choice.pk})

        self.assertEqual(response.status_code, 404)

    def test_vote_view_with_future_question_and_no_selected_choice(self):
        pub_date = timezone.now() + timezone.timedelta(days=30)
        question = self.create_question(pub_date=pub_date)

        url = reverse_lazy('polls:rdr-poll-vote', kwargs={'question_pk': question.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)

    def test_vote_view_with_old_question_and_selected_choice(self):
        pub_date = timezone.now() - timezone.timedelta(days=30)
        question = self.create_question(pub_date=pub_date)
        choice = question.choice_set.create(choice_text=self.faker.text(max_nb_chars=200))

        url = reverse_lazy('polls:rdr-poll-vote', kwargs={'question_pk': question.pk})
        response = self.client.post(url, {'choice_pk': choice.pk})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(question.choice_set.get(pk=choice.pk).votes, 1)

    def test_vote_view_with_old_question_and_no_selected_choice(self):
        pub_date = timezone.now() - timezone.timedelta(days=30)
        question = self.create_question(pub_date=pub_date)
        url = reverse_lazy('polls:rdr-poll-vote', kwargs={'question_pk': question.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error_message'], 'no choice selected')

