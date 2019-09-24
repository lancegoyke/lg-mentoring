from django import forms

from .models import Submission, Question

class SubmissionCreationForm(forms.Form):
    question_1 = forms.CharField(
        max_length=200,
        strip=True,
        required=True,
    )
    question_2 = forms.CharField(
        max_length=200,
        strip=True,
        required=True,
    )
    additional_notes = forms.CharField(
        max_length=1000,
        required=False,
        widget=forms.widgets.Textarea
    )
