import json
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
from questions.models import Question

# Import boto3 only if in production
if settings.ENVIRONMENT == "production":
    import boto3
    from boto3.session import Config
    from botocore.exceptions import ClientError


class Command(BaseCommand):
    help = "Exports mentoring data to a JSON file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-name",
            type=str,
            help="Custom name for the output file (without extension)",
            default=None,
        )
        parser.add_argument(
            "--chunk-size",
            type=int,
            help="Number of questions to process at once",
            default=100,
        )

    def handle(self, *args, **options):
        self.stdout.write("Starting data export...")

        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = options["output_name"] or f"mentoring_data_{timestamp}"
            json_filename = f"{filename}.json"

            # Process questions in chunks to manage memory
            chunk_size = options["chunk_size"]
            total_questions = Question.objects.count()
            self.stdout.write(
                f"Processing {total_questions} questions in chunks of {chunk_size}"
            )

            data = []
            for i in range(0, total_questions, chunk_size):
                questions_chunk = Question.objects.select_related("asker").order_by(
                    "date_asked"
                )[i : i + chunk_size]

                for question in questions_chunk:
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

                self.stdout.write(
                    f"Processed {min(i + chunk_size, total_questions)} of {total_questions} questions"
                )

            # Save the data
            json_data = json.dumps(data, indent=4)

            if settings.ENVIRONMENT == "production":
                # Upload to S3 in production
                self._upload_to_s3(json_data, json_filename)
            else:
                # Save locally in development
                with open(json_filename, "w") as f:
                    f.write(json_data)
                self.stdout.write(f"File saved locally as {json_filename}")

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully exported {len(data)} questions to {json_filename}"
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Export failed: {str(e)}"))
            raise

    def _upload_to_s3(self, json_data, filename):
        """Upload JSON data to S3 bucket"""
        try:
            # Get AWS region from settings
            aws_region = getattr(settings, "AWS_S3_REGION_NAME", "us-east-1")

            # Initialize S3 client with proper configuration
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=aws_region,
                config=Config(signature_version="s3v4"),
            )

            # Upload to S3
            s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=f"exports/{filename}",
                Body=json_data,
                ContentType="application/json",
            )

            # Generate presigned URL for download (valid for 1 hour)
            download_url = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
                    "Key": f"exports/{filename}",
                },
                ExpiresIn=3600,
            )

            self.stdout.write(
                f"File uploaded to S3: s3://{settings.AWS_STORAGE_BUCKET_NAME}/exports/{filename}"
            )
            self.stdout.write(f"Download URL (valid for 1 hour): {download_url}")

        except ClientError as e:
            self.stdout.write(self.style.ERROR(f"S3 upload failed: {str(e)}"))
            raise
