# Makefile

build:
	docker build . -t events_app

run:
	docker-compose up

run_dev:
	FLASK_ENV=development FLASK_APP=events_app.py FLASK_DEBUG=1 flask run