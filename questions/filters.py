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
            'question_text': ['contains'],
            'asker__first_name': ['contains',],
            'asker__last_name': ['contains',],
        }
