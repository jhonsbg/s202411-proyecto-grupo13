# syntax=docker/dockerfile:1
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install pipenv && pipenv install --deploy
EXPOSE 3000
LABEL author="h.maury@uniandes.edu.co"
ENTRYPOINT FLASK_APP=./src/main.py pipenv run flask run -h 0.0.0.0 -p 3000