from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import send_mail

from embed_video.fields import EmbedVideoField


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answer_url = models.URLField(blank=True)
    answer_video = EmbedVideoField(blank=True)
    answer_text = models.TextField(blank=True)
    date_asked = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    asker = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

    def get_absolute_url(self):
        return reverse("question_detail", args=[str(self.id)])

    def send_notification_email(self, email, user, url):
        # Notify the person who asked the question
        from_email = "noreply@lancegoyke.com"
        # Send to admin and user
        recipient_list = [
            "lance@lancegoyke.com",
            email,
        ]
        question_detail_view_url = url
        template_context = {
            "pk": self.pk,
            "user": user,
            "url": question_detail_view_url,
        }
        subject = render_to_string(
            template_name="questions/email/question_answered_email_notification_subject.txt"
        ).strip()
        message = render_to_string(
            template_name="questions/email/question_answered_email_notification_message.txt",
            context=template_context,
        )
        html_message = render_to_string(
            template_name="questions/email/question_answered_email_notification_message.html",
            context=template_context,
        )
        return send_mail(
            subject, message, from_email, recipient_list, html_message=html_message
        )


class Submission(models.Model):
    question_1 = models.CharField(max_length=200, default=None)
    post_question_1_anonymously = models.BooleanField(default=False)
    question_2 = models.CharField(max_length=200, blank=True)
    post_question_2_anonymously = models.BooleanField(default=False, blank=True)
    additional_notes = models.TextField(blank=True)
    submitted_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.submitted_by} [{self.date_submitted}]"

    def get_absolute_url(self):
        return reverse("question_filtered_list")
