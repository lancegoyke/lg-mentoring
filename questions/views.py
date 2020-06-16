from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.urls import reverse_lazy, reverse, get_script_prefix
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.forms import TextInput

from .filters import QuestionFilter

from .models import Question, Submission
from .forms import SubmissionCreationForm


def question_filtered_list(request):
    filter = QuestionFilter(
        request.GET, queryset=Question.objects.all().order_by('-date_asked'))
    return render(request, 'questions/question_filtered_list.html', {'filter': filter})


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'questions/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


'''
Use the UpdateView to add in answers.
'''


class QuestionUpdateView(UserPassesTestMixin, UpdateView):
    model = Question
    fields = ['question_text', 'answer_video',
              'answer_url', 'answer_text', 'is_published', ]
    template_name = 'questions/question_update.html'
    permission_denied_message = 'This page is only accessible by Administrators.'
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        if form.instance.is_published == True:
            form.instance.date_published = timezone.now()
            # Notify the person who asked the question
            from_email = 'noreply@lancegoyke.com'
            recipient_list = ['lance@lancegoyke.com',
                              self.request.user.email, ]
            question_detail_view_url = self.request.build_absolute_uri(
                reverse('question_detail', kwargs={'pk': self.get_object().pk}))
            template_context = {
                'pk': self.get_object().pk,
                'user': self.request.user,
                'url': question_detail_view_url
            }
            subject = render_to_string(
                template_name='questions/email/question_answered_email_notification_subject.txt'
            ).strip()
            message = render_to_string(
                template_name='questions/email/question_answered_email_notification_message.txt',
                context=template_context
            )
            html_message = render_to_string(
                template_name='questions/email/question_answered_email_notification_message.html',
                context=template_context
            )
            send_mail(subject, message, from_email,
                      recipient_list, html_message=html_message)
        return super(QuestionUpdateView, self).form_valid(form)


class SubmissionCreateView(CreateView):
    model = Submission
    fields = ['question_1', 'post_question_1_anonymously',
              'question_2', 'post_question_2_anonymously', 'additional_notes', ]
    template_name = 'questions/submission_create.html'

    def get_form(self):
        form = super().get_form()
        form.fields['question_2'].required = False
        form.fields['additional_notes'].required = False
        return form

    def form_valid(self, form):
        form.instance.submitted_by = self.request.user
        if form.instance.question_1:
            q1 = Question.objects.create(
                question_text=form.instance.question_1,
                asker=form.instance.submitted_by,
                is_anonymous=form.instance.post_question_1_anonymously
            )
        if form.instance.question_2:
            q2 = Question.objects.create(
                question_text=form.instance.question_2,
                asker=form.instance.submitted_by,
                is_anonymous=form.instance.post_question_2_anonymously
            )
        return super(SubmissionCreateView, self).form_valid(form)


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    model = Submission
    fields = ('question_1', 'question_2', 'additional_notes',)
