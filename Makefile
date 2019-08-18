# Makefile

run:
	FLASK_ENV=development FLASK_APP=events_app.py FLASK_DEBUG=1 flask run