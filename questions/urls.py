from django.urls import path

from .views import (
    QuestionDetailView,
    QuestionUpdateView,
    SubmissionCreateView,
    SubmissionDetailView,
    question_filtered_list,
)

urlpatterns = [
    path("<int:pk>/", QuestionDetailView.as_view(), name="question_detail"),
    path("<int:pk>/update/", QuestionUpdateView.as_view(), name="question_update"),
    path("submit/<int:pk>/", SubmissionDetailView.as_view(), name="submission_detail"),
    path("submit/", SubmissionCreateView.as_view(), name="submission_create"),
    path("", question_filtered_list, name="question_filtered_list"),
]
