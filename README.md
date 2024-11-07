# Mentoring

This app gathers submitted questions, publicizes then mentor's answer, and notifies the user via email.

It's pretty simple; lightweight and fast!

## Development

```
# Create virtual environment
uv venv

# Install dependencies
uv pip sync requirements.txt

# Start database
docker-compose up -d

# Start development server
python manage.py runserver

# run tests
python manage.py test
```

## Deploy

This project is deployed on Heroku. Every push to the `master` branch will deploy to Heroku automatically.

## Tech stack

- Docker Compose
- Python 3.11
- Django 4.1
- PostgreSQL
- SendGrid for SMTP
- Bootstrap for style
- Heroku for deployment
