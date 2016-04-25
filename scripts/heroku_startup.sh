#!/usr/bin/env bash
cd app
# Run Django migrations.
python manage.py migrate

# Start up the system
gunicorn scienceapi.wsgi:application
