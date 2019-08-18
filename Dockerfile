FROM python:3.6.9-alpine3.10

RUN apk add --no-cache build-base libffi-dev openssl libressl-dev musl-dev
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ENV FLASK_RUN_HOST 0.0.0.0
EXPOSE 5000
COPY . /app
ENV FLASK_ENV=development
ENV FLASK_APP=events_app.py
ENV FLASK_DEBUG=1
CMD bash

# docker build . -t events_app