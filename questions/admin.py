from django.contrib import admin

from embed_video.admin import AdminVideoMixin

from .models import Question, Submission


@admin.register(Submission)
class CustomSubmissionAdmin(admin.ModelAdmin):
    model = Submission
    list_display = [
        "submitted_by",
        "date_submitted",
        "question_1",
        "question_2",
    ]
    ordering = ("-date_submitted",)


@admin.register(Question)
class CustomQuestionAdmin(AdminVideoMixin, admin.ModelAdmin):
    model = Question
    list_display = [
        "asker",
        "date_asked",
        "question_text",
    ]
    ordering = ("-date_asked",)


