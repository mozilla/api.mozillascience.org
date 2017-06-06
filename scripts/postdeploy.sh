#!/usr/bin/env bash
cd app

# Run Django migrations.
python manage.py migrate

# Check if current deployment is a review app
if [ "$HEROKU_PARENT_APP_NAME" != "" ]
then
	# Seed database with dummy users
	python manage.py seedusers
fi
