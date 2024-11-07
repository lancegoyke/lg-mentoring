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

# deploy
heroku login
heroku git:remote -a lg-mentoring
git push heroku master
```

## Tech stack

- Docker Compose
- Python 3.11
- Django 4.1
- PostgreSQL
- SendGrid for SMTP
- Bootstrap for style
- Heroku for deployment
