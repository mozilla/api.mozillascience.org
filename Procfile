release: python app/manage.py migrate --no-input
web: cd app && gunicorn scienceapi.wsgi:application
