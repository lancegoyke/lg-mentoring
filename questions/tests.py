from django.db import IntegrityError
from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from .filters import QuestionFilter
from .models import Question, Submission


class QuestionTests(TestCase):

    user_username = "user"
    user_firstname = "John"
    user_lastname = "Doe"
    user_email = "user@email.com"
    user_password = "userpassword"
    superuser_username = "superuser"
    superuser_email = "superuser@email.com"
    superuser_password = "superuserpassword"

    def setUp(self):
        # Create users
        self.user = get_user_model().objects.create_user(
            first_name=self.user_firstname,
            last_name=self.user_lastname,
            username=self.user_username,
            email=self.user_email,
            password=self.user_password,
        )
        self.superuser = get_user_model().objects.create_superuser(
            username=self.superuser_username,
            email=self.superuser_email,
            password=self.superuser_password,
        )
        # Create questions
        self.public_question = Question.objects.create(
            question_text="New public question", asker=self.user, is_anonymous=False
        )
        self.anonymous_question = Question.objects.create(
            question_text="New private question", asker=self.user, is_anonymous=True
        )

    def test_public_question_listing(self):
        self.assertEqual(f"{self.public_question.question_text}", "New public question")
        self.assertEqual(f"{self.public_question.asker.email}", "user@email.com")
        self.assertEqual(self.public_question.is_anonymous, False)
        self.assertEqual(f"{self.public_question.answer_url}", "")
        self.assertEqual(f"{self.public_question.answer_text}", "")
        self.assertEqual(self.public_question.date_published, None)
        self.assertEqual(self.public_question.is_published, False)
        self.assertLessEqual(self.public_question.date_asked, timezone.now())

    def test_anonymous_question_listing(self):
        self.assertEqual(
            f"{self.anonymous_question.question_text}", "New private question"
        )
        self.assertEqual(f"{self.anonymous_question.asker.email}", "user@email.com")
        self.assertEqual(self.anonymous_question.is_anonymous, True)
        self.assertEqual(f"{self.anonymous_question.answer_url}", "")
        self.assertEqual(f"{self.anonymous_question.answer_text}", "")
        self.assertEqual(self.anonymous_question.date_published, None)
        self.assertEqual(self.anonymous_question.is_published, False)
        self.assertLessEqual(self.anonymous_question.date_asked, timezone.now())

    def test_question_list_view(self):
        response = self.client.get(reverse("question_filtered_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Filter questions")
        self.assertContains(response, "New public question")
        self.assertContains(response, "New private question")
        self.assertTemplateUsed(response, "questions/question_filtered_list.html")

    def test_public_question_detail_view(self):
        response = self.client.get(self.public_question.get_absolute_url())
        no_response = self.client.get("/q/fakeurlthatshouldbreak/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "New public question")
        self.assertContains(response, self.user_username)
        self.assertContains(response, "not yet been answered")
        self.assertTemplateUsed(response, "questions/question_detail.html")

    def test_anonymous_question_detail_view(self):
        response = self.client.get(self.anonymous_question.get_absolute_url())
        no_response = self.client.get("/q/fakeurlthatshouldbreak/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "New private question")
        self.assertContains(response, "Anonymous")
        self.assertContains(response, "not yet been answered")
        self.assertTemplateUsed(response, "questions/question_detail.html")

    def test_question_list_view_questiontextcontains_filter(self):
        qs = Question.objects.all()
        query = {"question_text__icontains": "public"}
        f = QuestionFilter(query, queryset=qs)
        self.assertQuerysetEqual(
            f.qs, [self.public_question.pk], lambda o: o.pk, ordered=False
        )

    def test_question_list_view_askerfirstnamecontains_filter(self):
        qs = Question.objects.all()
        query = {"asker__first_name__icontains": self.user_firstname}
        f = QuestionFilter(query, queryset=qs)
        self.assertQuerysetEqual(
            f.qs,
            [self.public_question.pk, self.anonymous_question.pk],
            lambda o: o.pk,
            ordered=False,
        )

    def test_question_list_view_askerlastnamecontains_filter(self):
        qs = Question.objects.all()
        query = {"asker__last_name__icontains": self.user_lastname}
        f = QuestionFilter(query, queryset=qs)
        self.assertQuerysetEqual(
            f.qs,
            [self.public_question.pk, self.anonymous_question.pk],
            lambda o: o.pk,
            ordered=False,
        )

    def test_question_update_view_does_not_allow_generic_user(self):
        self.client.login(username=self.user_username, password=self.user_password)
        response = self.client.get(self.public_question.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_question_update_view_allows_superuser(self):
        self.client.login(
            username=self.superuser_username, password=self.superuser_password
        )
        response = self.client.get(self.public_question.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_question_url(self):
        self.assertEqual(
            self.public_question.get_absolute_url(), f"/q/{self.public_question.pk}/"
        )

    # def test_question_update_view_sends_email(self):
    #     self.client.login(username=self.superuser_username, password=self.superuser_password)
    #     response = self.client.post(self.public_question.get_absolute_url(), {
    #         'question_text': 'New public question',
    #         'asker': self.user.pk,
    #         'is_anonymous': False,
    #         'answer_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    #         'answer_text': 'New public answer',
    #         'date_published': timezone.now(),
    #         'is_published': True
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(len(mail.outbox), 1)
    #     self.assertEqual(mail.outbox[0].subject, 'Your question has been answered!')


class SubmissionTests(TestCase):

    user_username = "user"
    user_email = "user@email.com"
    user_password = "userpassword"
    question_1 = "What is the best way to teach someone how to deadlift?"
    question_2 = "How can I convince a busy professional to work on their recovery?"

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username=self.user_username,
            email=self.user_email,
            password=self.user_password,
        )

    def test_submission_with_no_question(self):
        with self.assertRaises(IntegrityError):
            Submission.objects.create(submitted_by=self.user)

    def test_submission_with_one_question(self):
        submission = Submission.objects.create(
            question_1=self.question_1, submitted_by=self.user
        )
        self.assertEqual(submission.question_1, self.question_1)

    def test_submission_with_two_questions(self):
        submission = Submission.objects.create(
            question_1=self.question_1,
            question_2=self.question_2,
            submitted_by=self.user,
        )
        self.assertEqual(submission.question_1, self.question_1)
        self.assertEqual(submission.question_2, self.question_2)

    def test_additional_notes(self):
        submission = Submission.objects.create(
            question_1=self.question_1, submitted_by=self.user
        )
