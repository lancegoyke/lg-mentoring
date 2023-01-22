from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.sites.models import Site

from .filters import QuestionFilter

from .models import Question, Submission


def question_filtered_list(request):
    context = {}
    if request.user.is_anonymous:
        context["filter"] = QuestionFilter(
            request.GET, queryset=Question.objects.all().order_by("-date_asked")[:10]
        )
        context["num_questions"] = Question.objects.all().count()
    else:
        context["filter"] = QuestionFilter(
            request.GET, queryset=Question.objects.all().order_by("-date_asked")
        )
    return render(request, "questions/question_filtered_list.html", context)


class QuestionDetailView(DetailView):
    model = Question
    template_name = "questions/question_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class QuestionUpdateView(UserPassesTestMixin, UpdateView):
    """
    Use the UpdateView to add in answers.
    """

    model = Question
    fields = [
        "question_text",
        "answer_video",
        "answer_url",
        "answer_text",
        "is_published",
    ]
    template_name = "questions/question_update.html"
    permission_denied_message = "This page is only accessible by Administrators."
    login_url = reverse_lazy("login")

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        # Is the form becoming published?
        if (
            form.instance.is_published == True
            and self.get_object().is_published == False
        ):
            form.instance.date_published = timezone.now()
            email = self.request.user.email
            user = self.request.user
            domain = Site.objects.get_current().domain
            url = f"https://{domain}{self.object.get_absolute_url()}"
            self.object.send_notification_email(email, user, url)
        return super(QuestionUpdateView, self).form_valid(form)


class SubmissionCreateView(CreateView):
    model = Submission
    fields = [
        "question_1",
        "post_question_1_anonymously",
        "question_2",
        "post_question_2_anonymously",
        "additional_notes",
    ]
    template_name = "questions/submission_create.html"

    def form_valid(self, form):
        form.instance.submitted_by = self.request.user
        if form.instance.question_1:
            q1 = Question.objects.create(
                question_text=form.instance.question_1,
                asker=form.instance.submitted_by,
                is_anonymous=form.instance.post_question_1_anonymously,
            )
        if form.instance.question_2:
            q2 = Question.objects.create(
                question_text=form.instance.question_2,
                asker=form.instance.submitted_by,
                is_anonymous=form.instance.post_question_2_anonymously,
            )
        return super(SubmissionCreateView, self).form_valid(form)


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    fields = (
        "question_1",
        "question_2",
        "additional_notes",
    )
