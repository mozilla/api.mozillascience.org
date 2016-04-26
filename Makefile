build:
	docker-compose build

up: build
	docker-compose up -d
	docker attach apimozillascienceorg_web_1

test: build
	docker-compose run web sh -c "flake8 . && python /app/manage.py test"

migrate: build
	docker-compose run web python manage.py migrate

shell: build
	docker-compose run web python manage.py shell

cpenv:
	cp env.sample .env

createsuperuser:
	docker-compose run web python manage.py createsuperuser

cmigrate: build
	docker-compose run web ./manage.py makemigrations
