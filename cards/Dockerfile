# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y dos2unix && \
    pip install pipenv && \
    pipenv install --system --deploy

LABEL author="f.alarconf@uniandes.edu.co"

CMD ["/bin/sh", "-c", "export FLASK_APP=./src/main.py && flask run --port=3008 --host=0.0.0.0"]
