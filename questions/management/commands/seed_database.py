import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker
from questions.models import Question

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with sample data for users and questions."

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Initialize Faker
        fake = Faker()

        # --- Clean up existing data ---
        self.stdout.write("Clearing old data...")
        Question.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write("Old data cleared.")

        # --- Create Users ---
        self.stdout.write("Creating users...")
        # Create a superuser
        superuser, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "User",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            superuser.set_password("adminpass")
            superuser.save()
            self.stdout.write(
                self.style.SUCCESS(
                    'Superuser "admin" created with password "adminpass".'
                )
            )

        # Create regular users
        users = [superuser]
        for _ in range(5):
            first_name = fake.first_name()
            last_name = fake.last_name()
            user, created = User.objects.get_or_create(
                username=f"{first_name.lower()}.{last_name.lower()}",
                defaults={
                    "email": fake.email(),
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )
            if created:
                user.set_password("password")
                user.save()
            users.append(user)

        self.stdout.write(self.style.SUCCESS(f"Created {len(users)} users."))

        # --- Create Questions ---
        self.stdout.write("Creating questions...")
        questions_to_create = []
        for _ in range(20):
            asker = random.choice(users)
            is_published = random.choice([True, False])
            date_published = (
                fake.date_time_this_year(tzinfo=timezone.get_current_timezone())
                if is_published
                else None
            )

            # Only set video URL if the question is published
            answer_video = (
                f"https://vimeo.com/{random.randint(100000000, 999999999)}"
                if is_published
                else ""
            )

            questions_to_create.append(
                Question(
                    question_text=fake.sentence(nb_words=random.randint(5, 15))[:-1]
                    + "?",
                    asker=asker,
                    is_anonymous=random.choice([True, False]),
                    is_published=is_published,
                    date_published=date_published,
                    answer_text=fake.paragraph(nb_sentences=3) if is_published else "",
                    answer_video=answer_video,
                    answer_url=fake.url()
                    if is_published and random.choice([True, False])
                    else "",
                )
            )

        Question.objects.bulk_create(questions_to_create)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {len(questions_to_create)} questions."
            )
        )

        self.stdout.write(self.style.SUCCESS("Database seeding complete!"))
