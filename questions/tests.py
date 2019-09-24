from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Question

# Create your tests here.
class QuestionTests(TestCase):

    user_username = 'user'
    user_email = 'user@email.com'
    user_password = 'userpassword'
    superuser_username = 'superuser'
    superuser_email = 'superuser@email.com'
    superuser_password = 'superuserpassword'

    def setUp(self):
        # Create users
        self.user = get_user_model().objects.create_user(
            username=self.user_username,
            email=self.user_email,
            password=self.user_password
        )
        self.superuser = get_user_model().objects.create_superuser(
            username=self.superuser_username,
            email=self.superuser_email,
            password=self.superuser_password
        )
        # Create questions
        self.public_question = Question.objects.create(
            question_text='New public question',
            asker=self.user,
            is_anonymous=False
        )
        self.anonymous_question = Question.objects.create(
            question_text='New private question',
            asker=self.user,
            is_anonymous=True
        )

    def test_public_question_listing(self):
        self.assertEqual(f'{self.public_question.question_text}', 'New public question')
        self.assertEqual(f'{self.public_question.asker.email}', 'user@email.com')
        self.assertEqual(self.public_question.is_anonymous, False)
        self.assertEqual(f'{self.public_question.answer_url}', '')
        self.assertEqual(f'{self.public_question.answer_text}', '')
        self.assertEqual(self.public_question.date_published, None)
        self.assertEqual(self.public_question.is_published, False)
        self.assertLessEqual(self.public_question.date_asked, timezone.now())

    def test_anonymous_question_listing(self):
        self.assertEqual(f'{self.anonymous_question.question_text}', 'New private question')
        self.assertEqual(f'{self.anonymous_question.asker.email}', 'user@email.com')
        self.assertEqual(self.anonymous_question.is_anonymous, True)
        self.assertEqual(f'{self.anonymous_question.answer_url}', '')
        self.assertEqual(f'{self.anonymous_question.answer_text}', '')
        self.assertEqual(self.anonymous_question.date_published, None)
        self.assertEqual(self.anonymous_question.is_published, False)
        self.assertLessEqual(self.anonymous_question.date_asked, timezone.now())

    def test_question_list_view(self):
        response = self.client.get(reverse('question_filtered_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Filter Questions')
        self.assertContains(response, 'New public question')
        self.assertContains(response, 'New private question')
        self.assertTemplateUsed(response, 'questions/question_filtered_list.html')

    def test_question_list_view_questiontextcontains_filter(self):
        response = self.client.get(reverse('question_filtered_list') + '?question_text__contains=public')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'New public question')
        self.assertNotContains(response, 'New private question')

    def test_question_list_view_askerfirstnamecontains_filter(self):
        pass

    def test_question_list_view_askerlastnamecontains_filter(self):
        pass

    def test_public_question_detail_view(self):
        response = self.client.get(self.public_question.get_absolute_url())
        no_response = self.client.get('/q/fakeurlthatshouldbreak/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'New public question')
        self.assertContains(response, self.user_username)
        self.assertContains(response, 'not yet been answered')
        self.assertTemplateUsed(response, 'questions/question_detail.html')

    def test_anonymous_question_detail_view(self):
        response = self.client.get(self.anonymous_question.get_absolute_url())
        no_response = self.client.get('/q/fakeurlthatshouldbreak/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'New private question')
        self.assertContains(response, 'Anonymous')
        self.assertContains(response, 'not yet been answered')
        self.assertTemplateUsed(response, 'questions/question_detail.html')


class SubmissionTests(TestCase):

    def setUp(self):
        pass

    def test_submission_template(self):
        pass

    def test_submission_form(self):
        pass
