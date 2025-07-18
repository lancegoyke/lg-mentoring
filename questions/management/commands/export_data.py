import json
from django.core.management.base import BaseCommand
from questions.models import Question


class Command(BaseCommand):
    help = "Exports mentoring data to a JSON file."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data export...")

        data = []
        questions = Question.objects.all().order_by("date_asked")

        for question in questions:
            asker_info = {
                "username": question.asker.username,
                "first_name": question.asker.first_name,
                "last_name": question.asker.last_name,
                "email": question.asker.email,
            }

            question_data = {
                "question_text": question.question_text,
                "answer_text": question.answer_text,
                "answer_video_url": question.answer_video,
                "answer_url": question.answer_url,
                "date_asked": question.date_asked.isoformat()
                if question.date_asked
                else None,
                "date_published": question.date_published.isoformat()
                if question.date_published
                else None,
                "is_published": question.is_published,
                "is_anonymous": question.is_anonymous,
                "asker": asker_info,
            }
            data.append(question_data)

        with open("mentoring_data.json", "w") as f:
            json.dump(data, f, indent=4)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully exported {len(data)} questions to mentoring_data.json"
            )
        )
