# syntax=docker/dockerfile:1
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install pipenv && pipenv install --deploy
EXPOSE 3002
LABEL author="ma.munozb1@uniandes.edu.co"
ENTRYPOINT FLASK_APP=./src/main.py pipenv run flask run -h 0.0.0.0 -p 3002