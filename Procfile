web: cd mystery_backend && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn mystery_backend.wsgi:application --bind 0.0.0.0:$PORT
