# Generated by Django 4.0.7 on 2023-01-21 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "questions",
            "0016_alter_question_id_alter_submission_additional_notes_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="submission",
            name="question_1",
            field=models.CharField(default=None, max_length=200),
        ),
    ]
