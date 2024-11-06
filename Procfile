release: python manage.py migrate && python manage.py collectstatic --noinput
web: gunicorn mentoring_project.wsgi
