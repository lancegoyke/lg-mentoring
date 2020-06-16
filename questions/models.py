from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

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
        return reverse('question_detail', args=[str(self.id)])


class Submission(models.Model):
    question_1 = models.CharField(max_length=200)
    post_question_1_anonymously = models.BooleanField(default=False)
    question_2 = models.CharField(max_length=200)
    post_question_2_anonymously = models.BooleanField(default=False)
    additional_notes = models.TextField()
    submitted_by = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.submitted_by} [{self.date_submitted}]'

    def get_absolute_url(self):
        return reverse('question_filtered_list')
