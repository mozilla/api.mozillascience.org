build:
	docker-compose build

up: build
	docker-compose up

test: build
	docker-compose run web sh -c "pip install coverage flake8 && flake8 . && python /app/manage.py test"

migrate: build
	docker-compose run web python manage.py migrate

shell: build
	docker-compose run web python manage.py shell

env:
	cp env.sample .env

createsuperuser:
	docker-compose run web python manage.py createsuperuser
