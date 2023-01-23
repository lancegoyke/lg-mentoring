# Mentoring

This app gathers submitted questions, publicizes then mentor's answer, and notifies the user via email.

It's pretty simple; lightweight and fast!

## Development

```
# spin up Django development server
docker-compose up -d --build

# run tests
docker-compose exec web python manage.py test

# deploy
heroku login
git push heroku master
```

## Tech stack

* Docker Compose
* Python 3.11
* Django 4.1
* Pipenv
* PostgreSQL
* SendGrid for SMTP
* Bootstrap for style
* Heroku for deployment
