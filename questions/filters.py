import django_filters

from .models import Question

class QuestionFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        choices=(
            ('-date_asked', 'Newest First'),
            ('date_asked', 'Oldest First'),
        ),
        fields = {
            'date_asked': 'Date',
        }
    )

    class Meta:
        model = Question
        fields = {
            'question_text': ['icontains'],
            'asker__first_name': ['icontains',],
            'asker__last_name': ['icontains',],
        }
